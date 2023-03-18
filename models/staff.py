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


class Staff(models.Model):
    _name = 'hirms.staff'
    _description = 'staff of providers'
    _rec_name = 'provider_id'

    provider_id = fields.Many2one(
        comodel_name='hirms.provider',
        string='Provider',
        required=True
    )
    practitioner_id = fields.Many2one(
        comodel_name='hirms.practitioner',
        string='Practitioner',
        required=True
    )

    _sql_constraints = [
        (
            'staff_uniq',
            'unique(provider_id, practitioner_id)',
            'This practitioner already exist in the provider staff!'
        ),
    ]


class StaffWizard(models.Model):
    _name = 'hirms.staff.wizard'
    _description = 'Staff Wizard'

    provider_id = fields.Many2one(
        comodel_name='hirms.provider',
        string='Provider',
        required=True
    )
    practitioner_ids = fields.Many2many(
        comodel_name='hirms.practitioner',
        string='Provider Staff',
        domain=[
            ('is_provider', '=', True),
            ('is_generic', '=', False)
        ]
    )

    def record_staff(self):
        for record in self:
            provider_id = record.provider_id.id
            practitioners = record.practitioner_ids
            staff = self.env['hirms.staff']
            for practitioner in practitioners:
                staff.create({
                    'provider_id': provider_id,
                    'practitioner_id': practitioner.id,
                })
