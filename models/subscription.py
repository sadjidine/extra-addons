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


class Subscription(models.Model):
    _name = 'hirms.subscription'
    _description = 'Medical Insurance subscriptions'

    policy_id = fields.Many2one(
        comodel_name='hirms.policy',
        string='Policy',
        required=True
    )
    member_id = fields.Many2one(
        comodel_name='hirms.insured',
        string='Member',
        domain=[
            ('family_status', '=', 'member')
        ],
        required=True
    )
    ref_subscription = fields.Char(
        string="Ref. Subscription",
        compute='_get_ref_subscription',
        store=True,
    )
    start_date = fields.Date(
        string='Start Date',
        required=True,
    )
    end_date = fields.Date(
        string='End Date',
        required=False,
    )
    assigns_ids = fields.One2many(
        comodel_name='hirms.insured',
        inverse_name='subscription_id',
        string='Assigns',
        required=False
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
            'policy_member_uniq',
            'unique(policy_id, member_id)',
            'Policy for a member already exist and must be unique!'
        ),
    ]

    def name_get(self):
        res = []
        for rec in self:
            res.append(
                (rec.id,
                 "%s - %s" % (rec.ref_subscription, rec.name)
                 )
            )
        return res

    @api.depends('policy_id','member_id')
    def _get_ref_subscription(self):
        for rec in self:
            sid = rec.id
            pid = rec.policy_id.id
            if pid and isinstance(sid, int):
                ref = '%02d%04d' % (pid, sid)
                rec.ref_subscription = ref
                rec.ref_subscription


class SubscriptionWizard(models.TransientModel):
    _name = 'hirms.subscription.wizard'
    _description = 'Subscriptions wizard'

    firstname = fields.Char(string="First Name", size=128, required=True)
    lastname = fields.Char(string="Last Name", size=32, required=True)
    gender = fields.Selection(
        [
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        required=True,
    )
    date_birth = fields.Date(string='Date of Birth', required=True)
    administrative_ref = fields.Char(required=False)
    profession = fields.Char(string="Profession", help="Insured Occupation")
    external_id = fields.Char(
        string='External Id.',
        required=False
    )
    api_external_id = fields.Char(
        string='API External Id.',
        required=False
    )
    policy_id = fields.Many2one(
        comodel_name='hirms.policy',
        string='Policy',
        required=True
    )
    locality_id = fields.Many2one(
        comodel_name='hirms.locality',
        string='Locality',
        required=False,
    )
    organization_id = fields.Many2one(
        comodel_name='hirms.organization',
        string='Group unit',
        required=False
    )
    start_date = fields.Date(
        string='Start Date',
        required=False,
        help='Contract Start Date'
    )

    def subscription_wizard(self):
        member = self.env['hirms.insured']
        created_member = member.create(
            {
                'firstname': self.firstname,
                'lastname': self.lastname,
                'gender': self.gender,
                'date_birth': self.date_birth,
                'profession': self.profession,
                'external_id': self.external_id,
                'api_external_id': self.api_external_id,
                'policy_id': self.policy_id.id,
                'locality_id': self.locality_id.id,
                'organization_id': self.organization_id_id.id,
                'date_activation': self.start_date,

            }
        )

        member_id = created_member.id
        action = {
            'name': 'Create Member Subscription',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'hirms.subscription',
            'context': {
                'default_policy_id': self.policy_id.id,
                'default_member_id': member_id.id,
                'default_start_date': self.start_date,
            }
        }
        return action
