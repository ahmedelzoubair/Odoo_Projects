# -*- coding: utf-8 -*-
# from odoo import http


# class ConfirmationAuthority(http.Controller):
#     @http.route('/confirmation_authority/confirmation_authority', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/confirmation_authority/confirmation_authority/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('confirmation_authority.listing', {
#             'root': '/confirmation_authority/confirmation_authority',
#             'objects': http.request.env['confirmation_authority.confirmation_authority'].search([]),
#         })

#     @http.route('/confirmation_authority/confirmation_authority/objects/<model("confirmation_authority.confirmation_authority"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('confirmation_authority.object', {
#             'object': obj
#         })
