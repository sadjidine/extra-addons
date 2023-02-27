#-*- coding: utf-8 -*-

from odoo import http


class Hirms(http.Controller):
    @http.route('/hirms/insured', website=True, auth='public')
    def index(self, **kw):
        return '<h1 class="text-primary">Hello, world!</h1> <p>Ceci est un test...</p>'


    # @http.route('/hirms/hirms/objects', auth='public')
    # def list(self, **kw):
    #     return http.request.render('hirms.listing', {
    #         'root': '/hirms/hirms',
    #         'objects': http.request.env['hirms.hirms'].search([]),
    #     })

    # @http.route('/hirms/hirms/objects/<model("hirms.hirms"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('hirms.object', {
    #         'object': obj
    #     })
