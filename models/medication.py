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


class Molecule(models.Model):
    _name = 'hirms.molecule'
    _description = 'medication molecules'

    name = fields.Char(
        string="Molecule",
        size=128,
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
            'Molecule name must be unique'
        ),
    ]


class MedicationForm(models.Model):
    _name = 'hirms.medication.form'
    _description = 'Pharmaceutical forms medication'

    name = fields.Char(
        string="Medication Form",
        size=128,
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
            'Medication form name must be unique'
        ),
    ]



class TherapeuticRoute(models.Model):
    _name = 'hirms.therapeutic.route'
    _description = 'Therapeutic routes medication'

    name = fields.Char(
        size=128,
        required=True,
    )
    note = fields.Text(
        string="Note & description",
        required=False,
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Therapeutic route name must be unique'
        ),
    ]


class Medication(models.Model):
    _name = 'hirms.medication'
    _description = 'pharmacy drugs medication'

    name = fields.Char(
        string="Pharmaceutical Product",
        size=128,
        required=True,
        help="International Common Denomination..."
    )
    code = fields.Char(
        string="Product code",
        size=32,
    )
    dosage = fields.Char(
        size=32,
        help="Set the dosage of the pharmaceutical product"
    )
    indicative_price = fields.Float(
        digits=(6, 0),
        default=0
    )
    product_margin = fields.Float(
        digits=(6, 0),
        default=0,
        help="Set the tolerated margin of the pharmaceutical product price"
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
    molecule_ids = fields.Many2many(
        comodel_name="hirms.molecule",
        string="Molecules"
    )
    medication_form_id = fields.Many2one(
        comodel_name="hirms.medication.form",
        string="Medication Form",
        ondelete="set null",
    )
    therapeutic_route_id = fields.Many2one(
        comodel_name="hirms.therapeutic.route",
        string="Therapeutic Route",
        ondelete="set null",
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
            'name_form_therapeutic_uniq',
            'unique(name,medication_form_id,therapeutic_route_id)',
            'This Medication name, form and therapeutic route must be unique'
        ),
    ]

