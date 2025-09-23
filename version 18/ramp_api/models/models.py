from odoo import models, fields, api, _



# This custom model to integrate with Shipping company ( Creating API )
# Step One: To create new delivery methods named "Ramp" (sales => Configuration => Delivery Methods)
# Step Two: To create (new provider) inherit (delivery.carrier) model
class RampApi(models.Model):
    _inherit = "delivery.carrier"

    delivery_type = fields.Selection(
        selection_add=[('ramp_delivery', 'Ramp Delivery')],  # => add new option at field selection
        ondelete={'ramp_delivery': 'set default'}  # =>  If you later remove the 'ramp_delivery' option,
        # all existing delivery carriers that currently have delivery_type = 'ramp_delivery' will be automatically changed to the default value (which is 'fixed' in your case)
    )

    # The below fields will add at the Ramp Configuration tab
    ramp_api_key = fields.Char(string="Ramp API Key")
    ramp_api_url = fields.Char(string="Ramp API URL")
    ramp_tracking_endpoint = fields.Char(string="Ramp Tracking Endpoint")
    ramp_delivery_note = fields.Char(string="Ramp Delivery Note")
    ramp_lines = fields.One2many('delivery.carrier.lines', 'ramp_id')

    """
    Odoo uses dynamic method resolution based on [naming conventions]. 
When you call carrier.send_shipping(pickings) on a delivery carrier, Odoo doesn't just look for a method named send_shipping. Instead, it follows this pattern:

First, it checks the delivery_type field value (in your case: 'ramp_delivery')
Then, it dynamically constructs the method name: {delivery_type}_{method_name}
Finally, it calls: ramp_delivery_send_shipping(pickings)

You can see this pattern in the base delivery.carrier model in the rate_shipment method:

    """

    def ramp_delivery_send_shipping(self, pickings):
        """Send shipping request to Ramp API"""
        res = []
        for picking in pickings:
            # Generate tracking number
            tracking_number = f"RAMP{picking.id}{fields.Datetime.now().strftime('%Y%m%d%H%M')}"

            logmessage = f"Shipment sent to Ramp with tracking number: {tracking_number}"

            res.append({
                'exact_price': 0.0,  # You can calculate actual price here
                'tracking_number': tracking_number,
            })

            # Add message to picking
            picking.message_post(
                body=logmessage,
                message_type='notification'
            )

        return res

    def ramp_delivery_rate_shipment(self, order):
        """Rate shipment for Ramp delivery"""
        # Get delivery address city
        delivery_city = order.partner_shipping_id.city or order.partner_id.city

        if not delivery_city:
            return {
                'success': False,
                'price': 0.0,
                'error_message': 'Delivery city is required for Ramp delivery',
                'warning_message': False
            }

        # Find matching city in ramp_lines
        ramp_line = self.ramp_lines.filtered(lambda x: x.city.lower() == delivery_city.lower())

        if not ramp_line:
            return {
                'success': False,
                'price': 0.0,
                'error_message': f'Ramp delivery not available for city: {delivery_city}',
                'warning_message': False
            }

        return {
            'success': True,
            'price': ramp_line[0].price,
            'error_message': False,
            'warning_message': False
        }

    def ramp_delivery_get_tracking_link(self, picking):
        """Get tracking link for Ramp delivery"""
        if picking.carrier_tracking_ref and self.ramp_tracking_endpoint:
            return f"{self.ramp_tracking_endpoint}/{picking.carrier_tracking_ref}"
        return False

    def ramp_delivery_cancel_shipment(self, pickings):
        """Cancel shipment for Ramp delivery"""
        # Implement cancellation logic here if needed
        for picking in pickings:
            picking.message_post(body="Ramp shipment cancelled", message_type='notification')
        return True


class RampLines(models.Model):
    _name = "delivery.carrier.lines"
    _description = "Ramp Delivery Lines"

    ramp_id = fields.Many2one('delivery.carrier', ondelete='cascade')
    city = fields.Char(string="City", required=True)
    price = fields.Float(string="Price", required=True)


# Step Three: create a new button at warehouse delivery after validate
# To make :
# 1) Prepare data like API need to received
# 2) recall wizard view
class StockPicking(models.Model):
    _inherit = "stock.picking"

    # The below is button to create shipping request and open request wizard
    def picking_method(self):

        # Get the partner address
        # partner_address = ""
        # if self.partner_id:
        #     partner_address = self.partner_id._display_address()

        partner_address = ""
        if self.partner_id:
            address_parts = []
            if self.partner_id.street:
                address_parts.append(self.partner_id.street)
            if self.partner_id.street2:
                address_parts.append(self.partner_id.street2)
            if self.partner_id.city:
                address_parts.append(self.partner_id.city)
            if self.partner_id.state_id:
                address_parts.append(self.partner_id.state_id.name)
            if self.partner_id.zip:
                address_parts.append(self.partner_id.zip)
            if self.partner_id.country_id:
                address_parts.append(self.partner_id.country_id.name)

            partner_address = ", ".join(address_parts)

            # Get sale order total
            sale_total = 0.0
            if self.sale_id:
                sale_total = self.sale_id.amount_total

            # Prepare description
            description = ""
            if self.sale_id:
                sale_total = self.sale_id.amount_total

                # Generate description from sale order lines
                description_parts = []
                for line in self.sale_id.order_line:
                    if line.product_id and not line.is_delivery:  # Skip delivery lines
                        line_description = f"{line.product_id.name}: {line.product_uom_qty} x {line.price_unit} = {line.price_subtotal}"
                        description_parts.append(line_description)

                description = "; ".join(description_parts)

            # Prepare name of SO
            sales_order_seq = self.sale_id.name

        # call 'wizard' view and sending the preparing data with
        action = self.env.ref('ramp_api.action_create_shipping').read()[0]
        action['context'] = {
            'default_picking_id': self.id,  # Also pass the picking ID for reference
            'default_name': self.partner_id.name,
            'default_address': partner_address,
            'default_phone': self.partner_id.phone,
            'default_state': self.partner_id.state_id.name,
            'default_city': self.partner_id.city,
            'default_sale_total': sale_total,  # Pass the sale order total
            'default_description': description,
            'default_sale_name': sales_order_seq,
        }

        return action

    # The below to create filed for cont number at Shipping smart button
    ramp_response_ids = fields.One2many('ramp.api.response', 'picking_id', string="Ramp Responses")
    ramp_response_count = fields.Integer(string="Return Count", compute="_compute_ramp_response_count")

    @api.depends('ramp_response_ids')
    def _compute_ramp_response_count(self):
        for picking in self:
            picking.ramp_response_count = len(picking.ramp_response_ids)

    # #Step Six: create at stock picking smart button open form view contents a SUCCESS Response variables (labelURL,message,...)
    def json_response_smart_button(self):
        return {
            'name': _('Ramp Api Response'),
            'res_model': 'ramp.api.response',
            'view_mode': 'list,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id},
            'target': 'current',
            # open at the same page
            'type': 'ir.actions.act_window',
        }

    # The below is button to create return request and open return wizard
    def picking_method_return(self):

        # Get the partner address
        # partner_address = ""
        # if self.partner_id:
        #     partner_address = self.partner_id._display_address()

        partner_address = ""
        if self.partner_id:
            address_parts = []
            if self.partner_id.street:
                address_parts.append(self.partner_id.street)
            if self.partner_id.street2:
                address_parts.append(self.partner_id.street2)
            if self.partner_id.city:
                address_parts.append(self.partner_id.city)
            if self.partner_id.state_id:
                address_parts.append(self.partner_id.state_id.name)
            if self.partner_id.zip:
                address_parts.append(self.partner_id.zip)
            if self.partner_id.country_id:
                address_parts.append(self.partner_id.country_id.name)

            partner_address = ", ".join(address_parts)

            # Get sale order total
            sale_total = 0.0
            if self.sale_id:
                sale_total = self.sale_id.amount_total

            # Prepare description
            description = ""
            if self.sale_id:
                sale_total = self.sale_id.amount_total

                # Generate description from sale order lines
                description_parts = []
                for line in self.sale_id.order_line:
                    if line.product_id and not line.is_delivery:  # Skip delivery lines
                        line_description = f"{line.product_id.name}: {line.product_uom_qty} x {line.price_unit} = {line.price_subtotal}"
                        description_parts.append(line_description)

                description = "; ".join(description_parts)

            # Prepare name of SO
            sales_order_seq = self.sale_id.name

        # call 'wizard' view and sending the preparing data with
        action = self.env.ref('ramp_api.action_create_return').read()[0]
        action['context'] = {
            'default_picking_id': self.id,  # Also pass the picking ID for reference
            'default_name': self.partner_id.name,
            'default_address': partner_address,
            'default_phone': self.partner_id.phone,
            'default_state': self.partner_id.state_id.name,
            'default_city': self.partner_id.city,
            'default_sale_total': sale_total,  # Pass the sale order total
            'default_description': description,
            'default_sale_name': sales_order_seq,
        }

        return action

    # Create at stock picking smart button open form view contents a SUCCESS Return variables (labelURL,message,...)

    ramp_return_ids = fields.One2many('ramp.api.return', 'picking_id')
    ramp_return_count = fields.Integer(string="Return Count", compute="_compute_ramp_return_count")

    @api.depends('ramp_return_ids')
    def _compute_ramp_return_count(self):
        for picking in self:
            picking.ramp_return_count = len(picking.ramp_return_ids)

    def json_return_smart_button(self):
        return {
            'name': _('Ramp Api Return'),
            'res_model': 'ramp.api.return',
            'view_mode': 'list,form',
            'domain': [('picking_id', '=', self.id)],
            'context': {'default_picking_id': self.id},
            'target': 'current',
            # open at the same page
            'type': 'ir.actions.act_window',
        }


# Step Seven: I need to
# Create a model to store the API response data
# Update the wizard to save the response data

class RampApiResponse(models.Model):
    _name = "ramp.api.response"
    _description = "Ramp API Response"

    picking_id = fields.Many2one('stock.picking', string="Picking", required=True, ondelete='cascade')
    sale_number = fields.Char(string="Sale Number")
    labelURL = fields.Char(string="Label URL")
    message = fields.Char(string="Message")
    messageType = fields.Char(string="Message Type")
    packageStickerURL = fields.Char(string="Package Sticker URL")
    status = fields.Char(string="Status")
    trackingURL = fields.Char(string="Tracking URL")
    waybillNumber = fields.Char(string="Waybill Number")
    response_date = fields.Datetime(string="Response Date", default=fields.Datetime.now)


# Create a model to store the API return data
class RampApiReturn(models.Model):
    _name = "ramp.api.return"
    _description = "Ramp API Return"

    picking_id = fields.Many2one('stock.picking', string="Picking", required=True, ondelete='cascade')
    sale_number = fields.Char(string="Sale Number")
    labelURL = fields.Char(string="Label URL")
    message = fields.Char(string="Message")
    messageType = fields.Char(string="Message Type")
    packageStickerURL = fields.Char(string="Package Sticker URL")
    status = fields.Char(string="Status")
    trackingURL = fields.Char(string="Tracking URL")
    waybillNumber = fields.Char(string="Waybill Number")
    response_date = fields.Datetime(string="Response Date", default=fields.Datetime.now)
    return_type_new = fields.Selection([
        ('PACKAGEPICKUP', 'Package Pickup'),
        ('CASHREFUND', 'Cash Refund'),
        ('BOTH', 'Both'),
    ], string="Return Type", help="Select return type", readonly=1)
