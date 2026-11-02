# -*- coding: utf-8 -*-
# from odoo import http


# class MaxDiscPos(http.Controller):
#     @http.route('/max_disc_pos/max_disc_pos', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/max_disc_pos/max_disc_pos/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('max_disc_pos.listing', {
#             'root': '/max_disc_pos/max_disc_pos',
#             'objects': http.request.env['max_disc_pos.max_disc_pos'].search([]),
#         })

#     @http.route('/max_disc_pos/max_disc_pos/objects/<model("max_disc_pos.max_disc_pos"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('max_disc_pos.object', {
#             'object': obj
#         })

