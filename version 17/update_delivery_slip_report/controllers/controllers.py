# -*- coding: utf-8 -*-
# from odoo import http


# class UpdateDeliverySlipReport(http.Controller):
#     @http.route('/update_delivery_slip_report/update_delivery_slip_report', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/update_delivery_slip_report/update_delivery_slip_report/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('update_delivery_slip_report.listing', {
#             'root': '/update_delivery_slip_report/update_delivery_slip_report',
#             'objects': http.request.env['update_delivery_slip_report.update_delivery_slip_report'].search([]),
#         })

#     @http.route('/update_delivery_slip_report/update_delivery_slip_report/objects/<model("update_delivery_slip_report.update_delivery_slip_report"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('update_delivery_slip_report.object', {
#             'object': obj
#         })

