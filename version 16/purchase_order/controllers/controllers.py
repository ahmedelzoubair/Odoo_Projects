# -*- coding: utf-8 -*-
# from odoo import http


# class TestModule16(http.Controller):
#     @http.route('/test_module16/test_module16', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_module16/test_module16/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_module16.listing', {
#             'root': '/test_module16/test_module16',
#             'objects': http.request.env['test_module16.test_module16'].search([]),
#         })

#     @http.route('/test_module16/test_module16/objects/<model("test_module16.test_module16"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_module16.object', {
#             'object': obj
#         })
