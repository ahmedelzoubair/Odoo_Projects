# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesStates(models.Model):
    _inherit = 'sale.order'
