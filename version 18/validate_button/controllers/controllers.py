# -*- coding: utf-8 -*-
# from odoo import http


# class ValidateButton(http.Controller):
#     @http.route('/validate_button/validate_button', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/validate_button/validate_button/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('validate_button.listing', {
#             'root': '/validate_button/validate_button',
#             'objects': http.request.env['validate_button.validate_button'].search([]),
#         })

#     @http.route('/validate_button/validate_button/objects/<model("validate_button.validate_button"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('validate_button.object', {
#             'object': obj
#         })

