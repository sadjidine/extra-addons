# -*- coding: utf-8 -*-
#############################################################################
#
#    SIGEM (Société Ivoirienne d'Expertise, de Gestion et de Management.
#
#    Copyright (C) 2022-TODAY SIGEM(<https://www.sigem.pro>)
#    Author: Salifou OMBOTIMBE(<https://www.linkedin.com/in/ombotimbe-salifou-860a8044>)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from odoo import models, fields, api


class Decease(models.Model):
    _name = 'hirms.decease'
    _description = 'Insured deceases'

    name = fields.Char(
        string="Category",
        required=True,
    )
    insured_id = fields.Many2one(
        comodel_name='hirms.insured',
        string='Insured',
        required=True)
    date_decease = fields.Date(
        string='Decease Date',
        required=True)
    certificate_ref = fields.Char(
        string='Certificate ref.',
        required=True)
    date_certificate = fields.Date(
        string='Date of certificate',
        required=True)
    certificate_doc = fields.Binary(
        string="Scanned doc.",
        help="Please scan the certificate to join here."
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text('Note')

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Category name must be unique'
        ),
    ]

