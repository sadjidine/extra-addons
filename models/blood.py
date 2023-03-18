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
from odoo import models, fields


class Blood(models.Model):
    _name = 'hirms.blood'
    _description = 'Blood Group'
    _rec_name = 'blood_grp'

    blood_grp = fields.Char(string="Blood Group", required="True")
    note = fields.Text('Note')
    _sql_constraints = [
        ('unique_blood',
         'unique (blood_grp)',
         'Blood group already present!'
         )
    ]


class GeneticRisks(models.Model):
    _name = 'hirms.genetic.risks'
    _description = ' Genetic Risks'
    _rec_name = 'risks'

    risks = fields.Char(string="Genetic Risks", required="True")
    note = fields.Text('Note')
    _sql_constraints = [
        ('unique_risks',
         'unique (risks)',
         'This Genetic risks already present!'
         )
    ]
