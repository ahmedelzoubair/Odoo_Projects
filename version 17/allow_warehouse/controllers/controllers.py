# -*- coding: utf-8 -*-
# from odoo import http


# class AllowWarehouse(http.Controller):
#     @http.route('/allow_warehouse/allow_warehouse', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/allow_warehouse/allow_warehouse/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('allow_warehouse.listing', {
#             'root': '/allow_warehouse/allow_warehouse',
#             'objects': http.request.env['allow_warehouse.allow_warehouse'].search([]),
#         })

#     @http.route('/allow_warehouse/allow_warehouse/objects/<model("allow_warehouse.allow_warehouse"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('allow_warehouse.object', {
#             'object': obj
#         })

