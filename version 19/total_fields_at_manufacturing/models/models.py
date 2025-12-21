# -*- coding: utf-8 -*-

from odoo import models, fields, api

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    total_component_qty = fields.Float(
        string='Total Components',
        compute='_compute_total_component_qty',
        store=True,
        digits=(0,9)
    )

    @api.depends('bom_line_ids.product_qty')
    def _compute_total_component_qty(self):
        for bom in self:
            bom.total_component_qty = sum(bom.bom_line_ids.mapped('product_qty'))



class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    total_product_uom_qty = fields.Float(
        string='Total To Consume',
        compute='_compute_total_product_uom_qty',
        store=True,
        digits=(0,9),
        default=0.0
    )

    total_quantity = fields.Float(
        string='Total Consume',
        compute='_compute_total_quantity',
        store=True,
        digits=(0, 9),
        default=0.0
    )

    @api.depends('move_raw_ids.product_uom_qty')
    def _compute_total_product_uom_qty(self):
        for bom in self:
            bom.total_product_uom_qty = sum(bom.move_raw_ids.mapped('product_uom_qty'))


    @api.depends('move_raw_ids.quantity')
    def _compute_total_quantity(self):
        for bom in self:
            bom.total_quantity = sum(bom.move_raw_ids.mapped('quantity'))

