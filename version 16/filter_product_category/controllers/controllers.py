# -*- coding: utf-8 -*-
# from odoo import http


# class CompanyInCategory(http.Controller):
#     @http.route('/company_in_category/company_in_category', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/company_in_category/company_in_category/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('company_in_category.listing', {
#             'root': '/company_in_category/company_in_category',
#             'objects': http.request.env['company_in_category.company_in_category'].search([]),
#         })

#     @http.route('/company_in_category/company_in_category/objects/<model("company_in_category.company_in_category"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('company_in_category.object', {
#             'object': obj
#         })

