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


class Exercise(models.Model):
    _name = 'hirms.exercise'
    _description = 'administrative exercises'

    name = fields.Char(
        string="Exercise label",
        size=64,
        required=True,
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Organisation",
        required=False,
    )
    date_start = fields.Date(
        string="Start Date",
        required=True,
    )
    date_end = fields.Date(
        string="end Date",
        required=True,
    )
    medical_care_validity = fields.Integer(
        string="Process validity",
        default=0,
        help='Define the medical care process validity (in hours)'
    )
    medication_margin = fields.Float(
        string="Medication Margin",
        default=0,
        help='Define the medication margin tolerated for every pharmaceutical product price!'
    )
    closed = fields.Boolean(
        help="Checked to define this exercise to be closed!",
        default=False,
    )
    note = fields.Text(
        string="Note & description",
        required=False,
    )

    _sql_constraints = [
        (
            'name_organisation_uniq',
            'unique(name,company_id)',
            'Locality name must be unique for this department!'
        ),
        (
            'dates_check',
            'CHECK(date_start < date_end)',
            'The start date must be less than or equal to the end date!'
        ),
    ]

