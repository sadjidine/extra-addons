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


class Codification(models.Model):
    _name = 'hirms.codification'
    _description = 'medical codifications'

    name = fields.Char(
        string="Medical Code",
        required=True,
    )
    label = fields.Char(
        string="Code Label",
        required=False,
    )
    category_id = fields.Many2one(
        comodel_name="hirms.category",
        string="Related Category",
        ondelete="restrict",
        required=True,
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
            'label_uniq',
            'unique(label)',
            'Code Label must be unique'
        ),

    ]

