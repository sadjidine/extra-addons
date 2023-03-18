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
import TODO as TODO
from odoo import models, fields, api
from odoo.tools.translate import _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta


class HealthCare(models.Model):
    _name = 'hirms.healthcare'
    _description = 'medical Healthcare'

    doc_ref = fields.Char(
        required=False,
    )
    healthcare_seq = fields.Char(
        string='Healthcare Num.',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New')
    )
    insured_id = fields.Many2one(
        comodel_name='hirms.insured',
        string='Insured',
    )
    date_register = fields.Datetime(
        string='Register Date',
        default=fields.datetime.now,
        required=False
    )
    provider_id = fields.Many2one(
        comodel_name='res.partner',
        string='Provider',
        required=False,
    )
    member_id = fields.Many2one(
        comodel_name='hirms.insured',
        string='Member',
        required=False
    )
    pathology_id = fields.Many2one(
        comodel_name='hirms.pathology',
        string='Pathology',
        required=False,
        help="Select a pathology related (diagnostic)"
    )
    pathology_ids = fields.Many2many(
        comodel_name='hirms.pathology',
        string='Other Pathologies',
        relation='healthcare_pathologies',
    )
    state = fields.Selection(
        string='State',
        selection=[
            ('pending', 'Pending'),
            ('orientate', 'Orientation'),
            ('dispense', 'Dispensation'),
            ('expired', 'Expired'),
            ('Completed', 'Completed'),
        ],
        default='pending',
        required=True,
    )
    note = fields.Html('Note', sanitize_style=True)
    active = fields.Boolean(
        default=True,
    )

    _sql_constraints = [
        (
            'name_uniq',
            'unique(name)',
            'Category name must be unique'
        ),
    ]

    @api.model
    def create(self, vals):
        if vals.get('healthcare_seq', _('New')) == _('New'):
            vals['healthcare_seq'] = self.env['ir.sequence'].next_by_code(
                'hirms.healthcare') or _('New')
        result = super(HealthCare, self).create(vals)
        return result


class HealthcareLines(models.Model):
    _name = 'hirms.healthcare.lines'
    _description = 'Healthcare Lines'
    _order = 'date_execution'

    name = fields.Char()
    healthcare_id = fields.Many2one(
        comodel_name='hirms.healthcare',
        string='Healthcare',
        required=False
    )
    date_execution = fields.Date(
        string='Execution Date',
        required=False
    )
    date_demand = fields.Date(
        string='Demand Date',
        required=False
    )
    medicine_service_id = fields.Many2one(
        comodel_name='hirms.medicine.service',
        string='Medicine service',
        required=False
    )
    staff_id = fields.Many2one(
        comodel_name='hirms.staff',
        string='Staff',
        required=False
    )
    medication_id = fields.Many2one(
        comodel_name='hirms.medication',
        string='Medicament',
        required=False
    )
    substitute_id = fields.Many2one(
        comodel_name='hirms.medication',
        string='Substitute Medicament',
        required=False
    )
    complete_cover = fields.Boolean(
        string='Complete cover?',
        required=False,
        help='Checked to define the rate of refund to complete cover (100%)'
    )
    qty_demand = fields.Integer(
        string='Demand Qty.',
        required=False
    )
    quantity = fields.Integer(
        string='Quantity',
        required=False
    )
    dosage = fields.Char(
        string='Dosage',
        required=False
    )
    unit_price = fields.Monetary("Unit Price")
    currency_id = fields.Many2one(
        'res.currency',
        'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True
    )
    # COMPUTES FIELDS
    coverage = fields.Integer(
        string='Coverage(%)',
        required=False
    )
    sub_total = fields.Monetary('Sub-Total')
    pc_total = fields.Monetary('Process Care Total')
    npc_total = fields.Monetary('Non Process Care Total')
    third_party_payment = fields.Monetary('Third-party Payment')
    insured_fees = fields.Monetary('Insured fees')
    amount_due = fields.Monetary('Amount due')
    amount_payable = fields.Monetary('Amount payable')
    refund_amount = fields.Monetary('Reimbursement Amount')
    net_payable = fields.Monetary('Net payable')
    exclusion_amount = fields.Float(
        string='Exclusion amount',
        digits=(6, 0),
        required=False
    )
    exclusion_reason = fields.Text(
        string="Exclusion reason",
        required=False
    )


class HealthcareWizard(models.TransientModel):
    _name = 'hirms.healthcare.wizard'
    _description = 'Healthcare Wizard'

    entered_code = fields.Char(
        string='ID. Code',
        required=False,
        help='Please, enter a valid ID. code for insured.'
    )
    mcp_code = fields.Char(
        string='Medical Care Process Code',
        required=False,
        help='Please, enter a valid Medical Care Process code for insured.'
    )

    def new_process(self):
        user_id = self.env.context.get('uid')
        user = self.env['res.users'].search([('id', '=', user_id)])
        insured = self.env['hirms.insured'].search([(
            '|', '|', ('id_code', '=ilike', self.entered_code),
            ('external_id', '=ilike', self.entered_code),
            ('api_external_id', '=ilike', self.entered_code)
        )])
        provider = self.env['res.partner'].search([('id', '=', user.partner_id.id)])
        if len(insured) > 1:
            raise UserError(
                _("HIRMS: Business Rule Checks!\n\
                  ID. Code : %s is well and truly identified in the system.\
                  However, there is a duplicate of this ID. code.\
                  Please, contact the administrator for more information!")
                % self.entered_code
            )
        elif insured and not insured.police_id:
            raise UserError(
                _("HIRMS: Business Rule Checks!\n\
                  The insured: %s - ID. code: %s is indeed identified in the system.\
                  However, cannot currently be covered, for lack of a contract referring\
                  to its coverage policy.\n\
                  Please, contact the administrator for more information!")
            )
        # TODO: check insured state not active

        elif insured and insured.state == "active":
            id_code = insured.id_code
            if provider.is_provider:
                return {
                    'name': 'Register Insured Healthcare',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'hirms.healthcare',
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_insured_id': insured.id,
                        'default_id_code': id_code,
                        'default_provider_id': provider.id,
                    }
                }
            else:
                return {
                    'name': 'Register Insured Healthcare',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'res_model': 'hirms.healthcare',
                    'type': 'ir.actions.act_window',
                    'context': {
                        'default_insured_id': insured.id,
                        'default_id_code': id_code,
                    }
                }
        else:
            raise UserError(
                _("HIRMS: Business Rule Checks!\n\
                  The ID. code you provided is not a valid identifier in the system.\n\
                  Please, contact the administrator for more information!")
            )

    def update_process(self):
        pass
