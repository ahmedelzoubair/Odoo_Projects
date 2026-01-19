# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError


class PurchaseRequisition(models.Model):
    _inherit = 'purchase.requisition'

    def action_confirm(self):
        self.ensure_one()
        # Filter to only real product lines (exclude sections/notes)
        product_lines = self.line_ids.filtered(lambda l: not l.display_type)
        if not product_lines:
            raise UserError(
                _("You cannot confirm agreement '%(agreement)s' because it does not contain any product lines.",
                  agreement=self.name))
        if self.requisition_type == 'blanket_order':
            for requisition_line in product_lines:
                if requisition_line.price_unit <= 0.0:
                    raise UserError(_('You cannot confirm a blanket order with lines missing a price.'))
                if requisition_line.product_qty <= 0.0:
                    raise UserError(_('You cannot confirm a blanket order with lines missing a quantity.'))
                requisition_line._create_supplier_info()
        self.state = 'confirmed'


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    display_type = fields.Selection(
        selection=[
            ('line_section', 'Section'),
            ('line_note', 'Note'),
        ],
        default=False,
        help="Technical field for UX purpose."
    )

    name = fields.Text(string='Description')


    # Override product_id to remove the required constraint
    product_id = fields.Many2one(
        'product.product',
        string='Product',
        domain="[('purchase_ok', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        required=False  # Remove base requirement
    )

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to handle sections and notes"""
        for vals in vals_list:
            if vals.get('display_type') in ['line_section', 'line_note']:
                vals['product_id'] = False
                if 'product_qty' not in vals:
                    vals['product_qty'] = 0
                if 'price_unit' not in vals:
                    vals['price_unit'] = 0

        return super(PurchaseRequisitionLine, self).create(vals_list)

    def write(self, vals):
        """Override write to handle conversion between types"""
        if vals.get('display_type') in ['line_section', 'line_note']:
            vals.update({
                'product_id': False,
                'product_qty': 0,
                'price_unit': 0,
            })

        return super(PurchaseRequisitionLine, self).write(vals)

    @api.constrains('product_id', 'display_type')
    def _check_product_id_required_for_lines(self):
        """Ensure product is set for normal lines only"""
        for line in self:
            if not line.display_type and not line.product_id:
                raise ValidationError(_("Product is required for product lines."))

    @api.onchange('display_type')
    def _onchange_display_type(self):
        """Clear fields when switching to section/note"""
        if self.display_type in ['line_section', 'line_note']:
            self.product_id = False
            self.product_qty = 0
            self.price_unit = 0

    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        self.ensure_one()

        # Base values (will be overridden for sections/notes)
        vals = {
            'name': name or '',
            'product_id': self.product_id.id if self.product_id else False,
            'product_uom': self.product_id.uom_po_id.id if self.product_id else False,
            'product_qty': product_qty,
            'price_unit': price_unit,
            'taxes_id': [(6, 0, taxes_ids or [])],
            'date_planned': fields.Datetime.now(),
            'analytic_distribution': self.analytic_distribution,
            'display_type': self.display_type or False,
        }

        # Handle date planned
        if self.requisition_id.date_start:
            vals['date_planned'] = max(
                vals['date_planned'],
                fields.Datetime.to_datetime(self.requisition_id.date_start)
            )

        # Special handling for sections and notes
        if self.display_type in ('line_section', 'line_note'):
            # Use the 'name' field as the line description/title
            vals['name'] = self.name or (self.product_description_variants or 'Untitled')

            # Sections/notes should have no product, qty, price
            vals['product_id'] = False
            vals['product_uom'] = False
            vals['product_qty'] = 0.0
            vals['price_unit'] = 0.0
            vals['taxes_id'] = [(5, 0, 0)]  # clear taxes

            # Optional: make it stand out in PO
            if self.display_type == 'line_section':
                vals['name'] = vals['name']  # or use formatting you prefer
            elif self.display_type == 'line_note':
                vals['name'] = vals['name']

        else:
            # Normal product line: append description if any
            description = self.product_description_variants or ''
            if description:
                vals['name'] = f"{vals['name']}\n{description}"

        return vals

