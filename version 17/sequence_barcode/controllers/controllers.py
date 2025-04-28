# -*- coding: utf-8 -*-
# from odoo import http


# class SequenceBarcode(http.Controller):
#     @http.route('/sequence_barcode/sequence_barcode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sequence_barcode/sequence_barcode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sequence_barcode.listing', {
#             'root': '/sequence_barcode/sequence_barcode',
#             'objects': http.request.env['sequence_barcode.sequence_barcode'].search([]),
#         })

#     @http.route('/sequence_barcode/sequence_barcode/objects/<model("sequence_barcode.sequence_barcode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sequence_barcode.object', {
#             'object': obj
#         })

