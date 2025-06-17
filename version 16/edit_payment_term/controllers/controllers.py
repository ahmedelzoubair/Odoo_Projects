# -*- coding: utf-8 -*-
# from odoo import http


# class EditPaymentTerm(http.Controller):
#     @http.route('/edit_payment_term/edit_payment_term', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/edit_payment_term/edit_payment_term/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('edit_payment_term.listing', {
#             'root': '/edit_payment_term/edit_payment_term',
#             'objects': http.request.env['edit_payment_term.edit_payment_term'].search([]),
#         })

#     @http.route('/edit_payment_term/edit_payment_term/objects/<model("edit_payment_term.edit_payment_term"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('edit_payment_term.object', {
#             'object': obj
#         })
