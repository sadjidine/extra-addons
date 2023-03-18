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


class Standing(models.Model):
    _name = 'hirms.standing'
    _description = 'Provider\'s Standing'
    _rec_name = 'standing'

    standing = fields.Char(
        string="Standing",
        index=True,
        required=True,
    )

    _sql_constraints = [
        (
            'standing_uniq',
            'unique(standing)',
            'This Standing name already exist and must be unique!'
        ),
    ]


class ProviderStatus(models.Model):
    _name = 'hirms.provider.status'
    _description = 'Provider\'s Status'
    _rec_name = 'status'

    status = fields.Char(
        string="Status",
        index=True,
        required=True,
    )

    _sql_constraints = [
        (
            'status_uniq',
            'unique(status)',
            'This Standing name already exist and must be unique!'
        ),
    ]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    provider_type = fields.Many2one(
        comodel_name='hirms.provider.status',
        string='Provider type',
        required=False
    )
    staff_ids = fields.One2many(
        comodel_name='hirms.staff',
        inverse_name='provider_id',
        string='Medical Staff',
        required=False
    )
    service_ids = fields.One2many(
        comodel_name='hirms.medicine.service',
        inverse_name='provider_id',
        string='Offered Services',
        required=False
    )
    is_public = fields.Boolean(
        default=False,
        help="Checked to define if the provider is a public institution..."
    )
    is_provider = fields.Boolean(
        default=False,
        help="Checked to set partner as provider..."
    )
    is_generic = fields.Boolean(
        default=False,
        help="Checked to set partner as generic provider..."
    )
    is_practitioner = fields.Boolean(
        default=False,
        help="Checked to set partner as practitioner..."
    )
    is_member = fields.Boolean(
        default=False,
        help="Checked to set partner as member..."
    )
    is_assign = fields.Boolean(
        default=False,
        help="Checked to set partner as assign..."
    )
    date_agreement = fields.Date(
        string='Date of agreement',
        required=False,
    )
    currency_id = fields.Many2one(
        'res.currency',
        'Currency',
        default=lambda self: self.env.user.company_id.currency_id.id,
        required=True
    )
    deposit = fields.Monetary(
        "Deposit Amount",
        help="Type the deposit amount or default = 0",
    )
    pre_financing = fields.Monetary(
        "Pre-financing Amount",
        help="Type the amount of pre-financing or default = 0",
    )
    pre_financing_threshold = fields.Monetary(
        "Pre-financing Threshold",
        help="Type the amount of pre-financing threshold or default = 0",
    )
    discount_amount_pc = fields.Float(
        string='Discount Amount/Process'
    )
    discount_amount = fields.Float(
        string='Discount Amount/Invoice'
    )
    discount_percent_pc = fields.Float(
        string='Discount Percent/Process'
    )
    discount_percent = fields.Float(
        string='Discount Percent/Invoice'
    )


class MedicineService(models.Model):
    _name = 'hirms.medicine.service'
    _description = 'services offered by providers'
    _rec_name = 'provider_id'

    provider_id = fields.Many2one(
        comodel_name='hirms.provider',
        string='Provider',
        required=True
    )
    medicine_id = fields.Many2one(
        comodel_name='hirms.medicine',
        string='Medicine service',
        required=True
    )

    _sql_constraints = [
        (
            'service_uniq',
            'unique(provider_id, medicine_id)',
            'This medicine already exist in the provider services!'
        ),
    ]
