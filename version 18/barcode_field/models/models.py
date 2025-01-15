from odoo import models, fields, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    # One2many field to link product.product to stock.move
    product_relation_stock = fields.One2many(
        comodel_name='stock.move',  # Related model
        inverse_name='product_relation',  # Corresponding Many2one field in stock.move
        string="Related Stock Moves"
    )


# For Your Kindly Information, There is a direct relation between (stock.move) model and (stock.picking)
# The stock.move model has a Many2one field called picking_id that points back to the stock.picking model, like sale.order and sale.order.line :) .
class StockMove(models.Model):
    _inherit = "stock.move"

    # Many2one field to link stock.move to product.product
    product_relation = fields.Many2one(
        comodel_name='product.product',  # Related model
        string="Related Product"
    )

    # Related field to fetch the barcode from product.product
    barcode_product = fields.Char(
        string="Barcode",
        related='product_relation.barcode',  # Fetch barcode from product.product
        store=True,  # Optional: Store the value in the database for faster access
    )

    # Then override the create and write methods
    @api.model
    def create(self, vals):
        # Ensure product_relation is set when creating a new record
        if 'product_id' in vals and not vals.get('product_relation'):
            vals['product_relation'] = vals['product_id']
        return super(StockMove, self).create(vals)

    def write(self, vals):
        # Ensure product_relation is updated when product_id is updated
        if 'product_id' in vals:
            vals['product_relation'] = vals['product_id']
        return super(StockMove, self).write(vals)