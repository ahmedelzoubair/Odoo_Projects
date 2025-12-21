# -*- coding: utf-8 -*-
# from odoo import http


# class AnalyticDistributionAtPo(http.Controller):
#     @http.route('/analytic_distribution_at_po/analytic_distribution_at_po', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/analytic_distribution_at_po/analytic_distribution_at_po/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('analytic_distribution_at_po.listing', {
#             'root': '/analytic_distribution_at_po/analytic_distribution_at_po',
#             'objects': http.request.env['analytic_distribution_at_po.analytic_distribution_at_po'].search([]),
#         })

#     @http.route('/analytic_distribution_at_po/analytic_distribution_at_po/objects/<model("analytic_distribution_at_po.analytic_distribution_at_po"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('analytic_distribution_at_po.object', {
#             'object': obj
#         })

