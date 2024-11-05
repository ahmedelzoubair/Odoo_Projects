# -*- coding: utf-8 -*-
# from odoo import http


# class OmOdooInheriteence(http.Controller):
#     @http.route('/om_odoo_inheriteence/om_odoo_inheriteence', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/om_odoo_inheriteence/om_odoo_inheriteence/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('om_odoo_inheriteence.listing', {
#             'root': '/om_odoo_inheriteence/om_odoo_inheriteence',
#             'objects': http.request.env['om_odoo_inheriteence.om_odoo_inheriteence'].search([]),
#         })

#     @http.route('/om_odoo_inheriteence/om_odoo_inheriteence/objects/<model("om_odoo_inheriteence.om_odoo_inheriteence"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('om_odoo_inheriteence.object', {
#             'object': obj
#         })
