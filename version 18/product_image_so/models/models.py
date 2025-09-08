
from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_image = fields.Image(
        string='Image',
        related='product_id.image_1920'
    )


