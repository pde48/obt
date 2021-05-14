# -*- coding: utf-8 -*-
# from odoo import http


# class ManagmentObtBi(http.Controller):
#     @http.route('/managment_obt_bi/managment_obt_bi/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/managment_obt_bi/managment_obt_bi/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('managment_obt_bi.listing', {
#             'root': '/managment_obt_bi/managment_obt_bi',
#             'objects': http.request.env['managment_obt_bi.managment_obt_bi'].search([]),
#         })

#     @http.route('/managment_obt_bi/managment_obt_bi/objects/<model("managment_obt_bi.managment_obt_bi"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('managment_obt_bi.object', {
#             'object': obj
#         })
