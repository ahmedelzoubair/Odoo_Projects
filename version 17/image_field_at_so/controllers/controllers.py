# -*- coding: utf-8 -*-
# from odoo import http


# class ImageFieldAtSo(http.Controller):
#     @http.route('/image_field_at_so/image_field_at_so', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/image_field_at_so/image_field_at_so/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('image_field_at_so.listing', {
#             'root': '/image_field_at_so/image_field_at_so',
#             'objects': http.request.env['image_field_at_so.image_field_at_so'].search([]),
#         })

#     @http.route('/image_field_at_so/image_field_at_so/objects/<model("image_field_at_so.image_field_at_so"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('image_field_at_so.object', {
#             'object': obj
#         })

