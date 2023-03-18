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


class Degree(models.Model):
    _name = 'hirms.degree'
    _description = 'Practitioner\'s Degree'
    _rec_name = 'degree'

    degree = fields.Char(
        string="Practitioner's Degree",
        index=True,
        required=True,
    )

    _sql_constraints = [
        (
            'degree_uniq',
            'unique(degree)',
            'This degree already exist and must be unique!'
        ),
    ]


class Practitioner(models.Model):
    _name = 'hirms.practitioner'
    _description = 'Hirms Practitioners'
    _inherits = {'res.partner': "partner_id"}

    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade',
        index=True,
        required=True
    )
    degree_id = fields.Many2one(
        comodel_name='hirms.degree',
        string='Degree',
        index=True,
        required=True
    )
    specialization_id = fields.Many2one(
        comodel_name='hirms.specialization',
        string='Specialization',
        index=True,
        required=False
    )
    corp_ref = fields.Char(string="Corp. ref.", size=32, required=False)
    firstname = fields.Char(string="First Name", size=128, required=True)
    lastname = fields.Char(string="Last Name", size=32, required=True)
    fullname = fields.Char(string="FullName", compute="_get_full_name")
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        required=True,
    )

    @api.onchange('firstname', 'lastname')
    def _get_full_name(self):
        firstname = ''
        lastname = ''
        if self.firstname:
            firstname = self.firstname.lstrip().rstrip()
        if self.lastname:
            lastname = self.lastname.strip()
        self.name = "%s %s" % (lastname, firstname)
        self.fullname = self.name







