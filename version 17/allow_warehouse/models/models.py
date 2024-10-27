from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_warehouse_ids = fields.Many2many('stock.warehouse', string="Allowed Warehouses",
                                             help="Specify which warehouses this user is allowed to access."
                                             )

