# -*- coding: utf-8 -*-
# from odoo import http


# class OpeneducatExamInherit(http.Controller):
#     @http.route('/openeducat_exam_inherit/openeducat_exam_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/openeducat_exam_inherit/openeducat_exam_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('openeducat_exam_inherit.listing', {
#             'root': '/openeducat_exam_inherit/openeducat_exam_inherit',
#             'objects': http.request.env['openeducat_exam_inherit.openeducat_exam_inherit'].search([]),
#         })

#     @http.route('/openeducat_exam_inherit/openeducat_exam_inherit/objects/<model("openeducat_exam_inherit.openeducat_exam_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('openeducat_exam_inherit.object', {
#             'object': obj
#         })

