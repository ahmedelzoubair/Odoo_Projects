# -*- coding: utf-8 -*-
# from odoo import http


# class ProductImageSo(http.Controller):
#     @http.route('/product_image_so/product_image_so', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_image_so/product_image_so/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_image_so.listing', {
#             'root': '/product_image_so/product_image_so',
#             'objects': http.request.env['product_image_so.product_image_so'].search([]),
#         })

#     @http.route('/product_image_so/product_image_so/objects/<model("product_image_so.product_image_so"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_image_so.object', {
#             'object': obj
#         })

