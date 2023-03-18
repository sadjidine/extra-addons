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


class Schooling(models.Model):
    _name = 'hirms.schooling'
    _description = 'Child Schooling certificates'

    name = fields.Char(
        string="Category",
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
            'Category name must be unique'
        ),
    ]


class SchoolingWizard(models.TransientModel):
    _name = 'hirms.schooling.wizard'
    _description = 'Schooling Wizard'

    child_id_code = fields.Char(
        required=True,
        help="Please, provide identification code for the child."
    )

    def opem_popup(self):
        """
        This method is used to create a popup for the child schooling wizard.
        """
        self.ensure_one()
        insured = self.env['hirms.insured'].search([
            '|', ('id_code', '=ilike', self.child_id_code),
            ('external_id', '=ilike', self.child_id_code),
        ])
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'hirms.schooling',
            'view_id': self.child_id_code,
        }

