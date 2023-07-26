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
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta


class Insured(models.Model):
    _name = 'hirms.insured'
    _description = 'insured patients'
    _inherits = {'res.partner': "partner_id"}

    partner_id = fields.Many2one('res.partner', ondelete='cascade', required=True)
    policy_id = fields.Many2one(
        comodel_name='hirms.policy',
        string='Policy',
        required=True
    )
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
    date_birth = fields.Date(string='Date of Birth', required=True)
    date_decease = fields.Date(string='Date of decease', compute="_get_decease_date", store=True)
    date_registration = fields.Date(string='Date of registration', default=fields.Date.today())
    date_activation = fields.Date(string='Date of Activation', help='Date of activation')
    date_reactivation = fields.Date(string='Date of reactivation', help='Date of reactivation')
    administrative_ref = fields.Char(required=False)
    profession = fields.Char(string="Profession", help="Insured Occupation")
    id_code = fields.Char(
        string='Id. code',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        compute="_get_id_code",
        store=True,
        help="The system provides an incremental identification code for every created insured."
    )
    external_id = fields.Char(
        string='External Id.',
        required=False
    )
    api_external_id = fields.Char(
        string='API External Id.',
        required=False
    )

    family_status = fields.Selection(
        [
            ('member', 'Member'),
            ('conjunct', 'Conjunct'),
            ('child', 'Child'),
            ('other', 'Other')
        ],
        default="member",
        compute="_get_family_status",
        store=True,
    )
    relationship = fields.Selection(
        [
            ('conjunct', 'Conjunct'),
            ('child', 'Child'),
            ('other', 'Other')
        ],
        help="Select the corresponding status of insured in the family..."
    )
    locality_id = fields.Many2one(
        comodel_name='hirms.locality',
        string='Locality',
        required=False,
    )
    organization_id = fields.Many2one(
        comodel_name='hirms.organization',
        string='Organization unit',
        required=False
    )
    insured_seq = fields.Char(
        string='Insured Num.',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    # subscription_id = fields.Many2one(
    #     string='Member\'s Subscription',
    #     comodel_name='hirms.subscription',
    #     ondelete='restrict',
    #     index=True,
    # )
    member_id = fields.Many2one(
        comodel_name='hirms.insured',
        string='Member',
        ondelete='restrict',
        index=True,
        required=False
    )
    family_ids = fields.One2many(
        comodel_name='hirms.insured',
        inverse_name='member_id',
        string='Assigns',
        help="Assigns depending on member!"
    )
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    age_details = fields.Char(compute='_compute_age_details')
    weight = fields.Integer('Weight(kg)', help="The weight in Kilogram (kg)")
    height = fields.Integer('Height(cm)', help="The whight (in cemtimeter (cm)")
    bmi = fields.Float(
        string="BMI",
        digits=(4, 2),
        compute='_compute_bmi',
        help="Calculate the Body Mass Index"
    )
    bmi_result = fields.Char(compute='_get_bmi_result')
    blood_group = fields.Many2one('hirms.blood', string="Blood Group")
    risk_id = fields.Many2one('hirms.genetic.risks', "Genetic Risks")
    insured = fields.Boolean(
        default=True,
        help="Checked to set partner as insured..."
    )
    active = fields.Boolean(
        default=True,
    )
    note = fields.Html('Note', sanitize_style=True)

    def name_get(self):
        res = []
        for rec in self:
            rec_name = rec.name.strip()
            res.append((rec.id, "%s (%s)" % (rec_name, rec.id_code)))
        return res

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

    def _get_id_code(self):
        # self.ensure_one()
        for rec in self:
            if not rec.id_code and rec.name:
                name = rec.name.strip()
            name_tab = name.split(' ')
            sequence = rec.insured_seq[4:]
            if len(name_tab) > 1:
                rec.id_code = sequence + name_tab[0][0] + name_tab[1][0]

    @api.depends('relationship')
    def _get_family_status(self):
        """
        Get family status
        """
        for rec in self:
            if rec.relationship == 'conjunct':
                rec.family_status = 'conjunct'
            elif rec.relationship == 'child':
                rec.family_status = 'child'
            elif rec.relationship == 'other':
                rec.family_status = 'other'
            else:
                rec.family_status = 'member'

    def _get_decease_date(self):
        for rec in self:
            insured = self.env['hirms.decease'].search([
                ('insured_id', '=', rec.id)
            ])
            if insured:
                rec.date_decease = insured.date_decease

    @api.depends('date_birth')
    def _compute_age(self):
        """
        Age calculation of insured
        """
        for rec in self:
            rec.age = 0
            if rec.date_birth:
                age = int((date.today() - rec.date_birth) // timedelta(days=365.2425))
                rec.age = age

    @api.depends('date_birth')
    def _compute_age_details(self):
        """
        Details Age calculation of insured
        """
        now = datetime.now()
        for rec in self:
            dob = fields.Datetime.from_string(rec.date_birth)
            # deceased = True if rec.date_decease else False
            if bool(rec.date_decease):
                dod = fields.Datetime.from_string(rec.date_decease)
                delta = relativedelta(dod, dob)
                text = _('(deceased)')
            else:
                delta = relativedelta(now, dob)
                text = ''
            years = '%s' % delta.years
            years_month_days = '%s %s-%s %s-%s %s %s' % (
                delta.years, _('years'),
                delta.months, _('months'),
                delta.days, _('days'),
                text
            )
            rec.age_details = years_month_days

    @api.onchange('weight', 'height')
    def _compute_bmi(self):
        """
        BMI calculation
        """
        bmi = 0
        if self.weight > 0 and self.height > 0:
            bmi = (self.weight / ((self.height/100)**2))
        self.bmi = bmi

    @api.depends('bmi')
    def _get_bmi_result(self):
        for rec in self:
            result = ''
            if rec.bmi == 0:
                result = _('Unknown')
            elif rec.bmi < 18.5:
                result = _('Underweight')
            elif 18.5 <= rec.bmi <= 25:
                result = _('Normal weight')
            elif 25 < rec.bmi <= 30:
                result = _('Overweight')
            elif 30 < rec.bmi <= 35:
                result = _('Moderate obesity')
            elif 35 < rec.bmi <= 40:
                result = _('Severe obesity')
            elif rec.bmi > 40:
                result = _('Morbid obesity')
            rec.bmi_result = result

    @api.model
    def create(self, vals):
        if vals.get('insured_seq', _('New')) == _('New'):
            vals['insured_seq'] = self.env['ir.sequence'].next_by_code(
                'hirms.insured') or _('New')
        result = super(Insured, self).create(vals)
        return result


class SubscriptionWizard(models.TransientModel):
    _name = 'hirms.subscription.wizard'
    _description = 'Subscriptions wizard'

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
    date_birth = fields.Date(string='Date of Birth', required=True)
    age = fields.Integer(string="Age", compute='_compute_age')
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

    @api.onchange('firstname', 'lastname')
    def _get_full_name(self):
        firstname = ''
        lastname = ''
        if self.firstname:
            firstname = self.firstname.lstrip().rstrip()
        if self.lastname:
            lastname = self.lastname.strip()
        self.fullname  = "%s %s" % (lastname, firstname)

    @api.depends('date_birth')
    def _compute_age(self):
        """
        Age calculation of insured
        """
        for rec in self:
            rec.age = 0
            if rec.date_birth:
                age = int((date.today() - rec.date_birth) // timedelta(days=365.2425))
                rec.age = age

    def subscription_wizard(self):
        member = self.env['hirms.insured']
        created_member = member.create(
            {
                'firstname': self.firstname,
                'lastname': self.lastname,
                'name': self.fullname,
                'gender': self.gender,
                'date_birth': self.date_birth,
                'profession': self.profession,
                'external_id': self.external_id,
                'api_external_id': self.api_external_id,
                'policy_id': self.policy_id.id,
                'locality_id': self.locality_id.id if self.locality_id.id else '',
                'organization_id': self.organization_id_id.id if self.organization_id.id else '',
                'member': True,
                'date_activation': self.start_date,

            }
        )
        member_id = created_member.id
        res_id = self.env['hirms.insured'].search([('id', '=', member_id)]).id
        view_id = self.env.ref('hirms.member_form', False).id
        action = {
            'name': 'Create Member Subscription',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current',
            'views': [(view_id, 'form')],
            'res_model': 'hirms.insured',
            'view_id': view_id,
            'res_id': res_id,
            'context': {
                # 'default_member_id': active_id,
            }
        }
        return action


