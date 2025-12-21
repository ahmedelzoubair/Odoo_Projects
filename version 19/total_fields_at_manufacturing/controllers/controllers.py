# -*- coding: utf-8 -*-
# from odoo import http


# class TotalFieldForProductQty(http.Controller):
#     @http.route('/total_field_for_product_qty/total_field_for_product_qty', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/total_field_for_product_qty/total_field_for_product_qty/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('total_field_for_product_qty.listing', {
#             'root': '/total_field_for_product_qty/total_field_for_product_qty',
#             'objects': http.request.env['total_field_for_product_qty.total_field_for_product_qty'].search([]),
#         })

#     @http.route('/total_field_for_product_qty/total_field_for_product_qty/objects/<model("total_field_for_product_qty.total_field_for_product_qty"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('total_field_for_product_qty.object', {
#             'object': obj
#         })

