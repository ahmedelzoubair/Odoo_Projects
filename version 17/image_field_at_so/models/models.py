# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ImageFieldAtSO(models.Model):
    _inherit = 'sale.order.line'

    image = fields.Binary(string="Image",related='product_id.product_tmpl_id.image_1920',store=True)

