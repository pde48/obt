# -*- coding: utf-8 -*-
from odoo import http

# class ObtBi(http.Controller):
#     @http.route('/obt_bi/obt_bi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/obt_bi/obt_bi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('obt_bi.listing', {
#             'root': '/obt_bi/obt_bi',
#             'objects': http.request.env['obt_bi.obt_bi'].search([]),
#         })

#     @http.route('/obt_bi/obt_bi/objects/<model("obt_bi.obt_bi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('obt_bi.object', {
#             'object': obj
#         })