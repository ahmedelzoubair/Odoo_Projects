# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AddFieldsLengthWidthCostM2Product(models.Model):
    _inherit = 'product.template'

    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    price_per_meter = fields.Float(string="Price Per Meter (m2)")
    cost_per_meter = fields.Float(string="Cost Per Meter (m2)")


class AddFieldsLengthWidthCostM2Variants(models.Model):
    _inherit = 'product.product'

    length = fields.Float(string="Length")
    width = fields.Float(string="Width")
    cost_per_meter = fields.Float(string="Cost Per Meter (m2)")
    price_per_meter = fields.Float(string="Price Per Meter (m2)")

class AddFieldsAtPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    cost_per_meter = fields.Float(string="Cost m2", related='product_id.cost_per_meter')

    # the below div to make the calculation
    @api.depends('product_id', 'product_qty', 'cost_per_meter', 'product_id.length', 'product_id.width',
                 'product_id.product_tmpl_id.length', 'product_id.product_tmpl_id.width')
    def _compute_price_unit(self):
        """
        Compute price_unit based on length, width, and cost_per_meter.
        Fallback to product.template if product.product fields are not available.
        """
        for line in self:
            if line.product_id and line.cost_per_meter:
                # Fetch length and width from product.product
                length = line.product_id.length
                width = line.product_id.width

                # If not defined in product.product, fallback to product.template
                if not length or not width:
                    length = line.product_id.product_tmpl_id.length
                    width = line.product_id.product_tmpl_id.width

                # Calculate price_unit if all values are present
                if length and width and line.cost_per_meter:
                    line.price_unit = length * width * line.cost_per_meter
                else:
                    # If any value is missing, keep the default price_unit
                    line.price_unit = line.price_unit or 0.0

    price_unit = fields.Float(compute="_compute_price_unit", store=True)

class AddFieldsAtSalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # Custom calculation of price_unit based on length, width, and price_per_meter
    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_calculate_price_unit(self):
        """
        Custom calculation for price_unit based on length, width, and price_per_meter
        from either product.product or product.template.
        """
        for line in self:
            if line.product_id:
                # Fetch length, width, and price_per_meter from product.product (variant)
                length = line.product_id.length
                width = line.product_id.width
                price_per_meter = line.product_id.price_per_meter

                # Fallback to product.template if product.product fields are not set
                if not length or not width or not price_per_meter:
                    length = line.product_id.product_tmpl_id.length
                    width = line.product_id.product_tmpl_id.width
                    price_per_meter = line.product_id.product_tmpl_id.price_per_meter

                # Check if length, width, and price_per_meter are present before calculating price_unit
                if length and width and price_per_meter:
                    # Custom calculation for price_unit based on dimensions and price_per_meter
                    line.price_unit = length * width * price_per_meter
                else:
                    # If any required field is missing, retain the default price_unit
                    line.price_unit = line.price_unit