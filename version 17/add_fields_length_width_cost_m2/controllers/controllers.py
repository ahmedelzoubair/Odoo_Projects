# -*- coding: utf-8 -*-
# from odoo import http


# class AddFieldsLengthWidthCostM2(http.Controller):
#     @http.route('/add_fields_length_width_cost_m2/add_fields_length_width_cost_m2', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_fields_length_width_cost_m2/add_fields_length_width_cost_m2/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_fields_length_width_cost_m2.listing', {
#             'root': '/add_fields_length_width_cost_m2/add_fields_length_width_cost_m2',
#             'objects': http.request.env['add_fields_length_width_cost_m2.add_fields_length_width_cost_m2'].search([]),
#         })

#     @http.route('/add_fields_length_width_cost_m2/add_fields_length_width_cost_m2/objects/<model("add_fields_length_width_cost_m2.add_fields_length_width_cost_m2"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_fields_length_width_cost_m2.object', {
#             'object': obj
#         })

