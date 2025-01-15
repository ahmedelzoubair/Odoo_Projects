# -*- coding: utf-8 -*-
# from odoo import http


# class BarcodeField(http.Controller):
#     @http.route('/barcode_field/barcode_field', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/barcode_field/barcode_field/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('barcode_field.listing', {
#             'root': '/barcode_field/barcode_field',
#             'objects': http.request.env['barcode_field.barcode_field'].search([]),
#         })

#     @http.route('/barcode_field/barcode_field/objects/<model("barcode_field.barcode_field"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('barcode_field.object', {
#             'object': obj
#         })

