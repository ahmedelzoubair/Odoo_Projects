# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class update_delivery_slip_report(models.Model):
#     _name = 'update_delivery_slip_report.update_delivery_slip_report'
#     _description = 'update_delivery_slip_report.update_delivery_slip_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

