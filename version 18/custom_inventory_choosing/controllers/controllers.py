# -*- coding: utf-8 -*-
# from odoo import http


# class CustomInventoryChoosing(http.Controller):
#     @http.route('/custom_inventory_choosing/custom_inventory_choosing', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_inventory_choosing/custom_inventory_choosing/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_inventory_choosing.listing', {
#             'root': '/custom_inventory_choosing/custom_inventory_choosing',
#             'objects': http.request.env['custom_inventory_choosing.custom_inventory_choosing'].search([]),
#         })

#     @http.route('/custom_inventory_choosing/custom_inventory_choosing/objects/<model("custom_inventory_choosing.custom_inventory_choosing"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_inventory_choosing.object', {
#             'object': obj
#         })

