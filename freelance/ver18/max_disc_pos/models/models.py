# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class max_disc_pos(models.Model):
#     _name = 'max_disc_pos.max_disc_pos'
#     _description = 'max_disc_pos.max_disc_pos'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

