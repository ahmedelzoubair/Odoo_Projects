# -*- coding: utf-8 -*-
# from odoo import http


# class ApplyButton(http.Controller):
#     @http.route('/apply_button/apply_button', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/apply_button/apply_button/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('apply_button.listing', {
#             'root': '/apply_button/apply_button',
#             'objects': http.request.env['apply_button.apply_button'].search([]),
#         })

#     @http.route('/apply_button/apply_button/objects/<model("apply_button.apply_button"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('apply_button.object', {
#             'object': obj
#         })
