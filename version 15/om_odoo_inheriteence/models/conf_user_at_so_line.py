# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    confirmed_user_id_soLine = fields.Many2one('res.users',string="Confirmed User",related='order_id.confirmed_user_id',store=True)
    # Note:- 1st of all to make a relation between two models we need to create same field category (if the two field must be same field type)
    # related='order_id.confirmed_user_id' :- There is a relation between two model by default [order_id = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade')]
    # so the (order_id) is the relation filed between two model

    line_number = fields.Integer(string="Line Num")