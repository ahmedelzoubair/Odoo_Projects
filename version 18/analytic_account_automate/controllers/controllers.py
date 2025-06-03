# -*- coding: utf-8 -*-
# from odoo import http


# class AnalyticAccountAutomate(http.Controller):
#     @http.route('/analytic_account_automate/analytic_account_automate', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/analytic_account_automate/analytic_account_automate/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('analytic_account_automate.listing', {
#             'root': '/analytic_account_automate/analytic_account_automate',
#             'objects': http.request.env['analytic_account_automate.analytic_account_automate'].search([]),
#         })

#     @http.route('/analytic_account_automate/analytic_account_automate/objects/<model("analytic_account_automate.analytic_account_automate"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('analytic_account_automate.object', {
#             'object': obj
#         })

