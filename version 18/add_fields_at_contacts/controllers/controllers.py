# -*- coding: utf-8 -*-
# from odoo import http


# class AddFieldsAtContacts(http.Controller):
#     @http.route('/add_fields_at_contacts/add_fields_at_contacts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/add_fields_at_contacts/add_fields_at_contacts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('add_fields_at_contacts.listing', {
#             'root': '/add_fields_at_contacts/add_fields_at_contacts',
#             'objects': http.request.env['add_fields_at_contacts.add_fields_at_contacts'].search([]),
#         })

#     @http.route('/add_fields_at_contacts/add_fields_at_contacts/objects/<model("add_fields_at_contacts.add_fields_at_contacts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('add_fields_at_contacts.object', {
#             'object': obj
#         })

