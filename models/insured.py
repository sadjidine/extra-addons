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
from odoo.tools.populate import compute
from odoo.tools.translate import _


class Insured(models.Model):
    _name = 'hirms.insured'
    _description = 'insured patients'
    _inherits = {'res.partner': "partner_id"}

    partner_id = fields.Many2one(
        'res.partner',
        ondelete='cascade',
        required=True,
    )
    # firstName = fields.Char(
    #     string='First name'
    # )
    # lastName = fields.Char(
    #     string='Last name'
    # )
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
        ]
    )
    dob = fields.Date(
        string='Date of Birth',
        required=True,
    )
    dor = fields.Date(
        string='Date of registration',
        default=fields.Date.today(),
    )
    doreact = fields.Date(
        string='Date of reactivation',
        help='Date of reactivation',
    )
    dod = fields.Date(
        string='Date of death'
    )
    relationship = fields.Selection(
        [
            ('member', 'Member'),
            ('conjunct', 'Conjunct'),
            ('child', 'Child'),
            ('other', 'Other')
        ]
    )
    bloodGroup = fields.Selection(
        [
            ('A+', 'A+'),
            ('A-', 'A-'),
            ('B+', 'B+'),
            ('B-', 'B-'),
            ('AB+', 'AB+'),
            ('AB-', 'AB-'),
            ('O+', 'O+'),
            ('O-', 'O-'),
        ],
        help='Select the blood group in the list of blood groups!'
    )
    insured_seq = fields.Char(
        string='Insured No.',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    parent_id = fields.Many2one(
        string='Related member',
        comodel_name='hirms.insured',
        ondelete='restrict',
        index=True,
    )
    
    child_ids = fields.One2many(
        comodel_name='hirms.insured',
        inverse_name='parent_id',
        string='Assigns',
        help="Assigns depending on member!"
    )
    active = fields.Boolean(
        default=True,
    )

    @api.depends('name')
    def _compute_name(self):
        for rec in self:
            if rec.name:
                rec.name = rec.firstName.strip() + ' ' + rec.lastName.strip()

    def name_get(self):
        res = []
        for rec in self:
            rec_name = rec.name.strip()
            res.append((rec.id, "%s (%s)" % (rec_name, rec.insured_seq)))
        return res

    @api.model
    def create(self, vals):
        if vals.get('insured_seq', _('New')) == _('New'):
            vals['insured_seq'] = self.env['ir.sequence'].next_by_code(
                'hirms.insured') or _('New')
        result = super(Insured, self).create(vals)
        return result
