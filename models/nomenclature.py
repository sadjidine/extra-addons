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


class Nomenclature(models.Model):
    _name = 'hirms.nomenclature'
    _description = 'nomenclature of medical procedures'

    name = fields.Char(
        string='Nomenclature',
        required=True,
    )
    code = fields.Char(
        required=False,
        help="Set if necessary, the code of this medical procedure!"
    )
    codification_id = fields.Many2one(
        comodel_name="hirms.codification",
        string="Related Codification",
        ondelete="restrict",
        required=True,
    )
    coefficient = fields.Integer(
        default=1,
    )
    prior_agreement = fields.Boolean(
        help="Checked if this procedure need the prior agreement of medical practitioner",
    )
    editable_cost = fields.Boolean(
        help="Checked if the cost of this procedure is editable and not set by default!",
    )
    quantity_required = fields.Boolean(
        help="Checked if the quantity of this procedure is required!",
    )
    pending_period = fields.Integer(
        default=0,
        help="Set the waiting period (timeout) in days, between 2 procedures for this nomenclature!"
    )
    minimum_age = fields.Integer(
        default=0,
        help="Set the minimum patient age required for this medical procedure!"
    )
    maximum_age = fields.Integer(
        default=0,
        help="Set the maximum patient age required for this medical procedure!"
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Text(
        string="Note & description",
        required=False,
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Codification name must be unique'
        ),
        (
            'code_uniq',
            'unique(code)',
            'Code Label must be unique'
        ),

    ]

