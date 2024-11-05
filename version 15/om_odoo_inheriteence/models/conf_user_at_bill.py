# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResGroups(models.Model):
    _inherit = 'account.move'

    sale_order_id = fields.Many2one('sale.order',string="sale order related field")
    # confirmed_user_id_so = fields.Char(string="SO Confirmed User", related='sale_order_id.confirmed_user_id')
    """""
    when i try to use the previous relation face an error:
    TypeError: Type of related field account.move.confirmed_user_id_so is inconsistent with sale.order.confirmed_user_id - - -
    Because:
    In my code:
        confirmed_user_id_so is defined as a fields.Char in account.move.
        confirmed_user_id in sale.order is likely defined as a Many2one relationship to res.users.
    To fix this:
    I should define confirmed_user_id_so as a Many2one field pointing to res.users to match the field type of confirmed_user_id.
    confirmed_user_id_so = fields.Many2one('res.users',string="SO Confirmed User",related='sale_order_id.confirmed_user_id',store=True)
    BUT the relation will not work until call super _prepare_invoice def at sale.order model 
    """""
    confirmed_user_id_so = fields.Many2one(
        'res.users',
        string="SO Confirmed User",
        related='sale_order_id.confirmed_user_id', store=True)


class ResGroupsLine(models.Model):
    _inherit = 'account.move.line'

    confirmed_user_id_so_line = fields.Many2one(
        'res.users',
        string="SO Confirmed User",
        related='move_id.confirmed_user_id_so', store=True)

    line_number= fields.Integer(string="Line Num")





