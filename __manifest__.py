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
{
    'name': "HIRMS",
    'description': """
    Healthcare Insurance Records Management System.
    """,
    'summary': """
    HIRMS module which is used to mange the healthcare insurance functionalities prescription,
    patient,doctor diagnosis etc
    """,
    'author': "SIGEM",
    'company': "SIGEM",
    'maintainer': 'Salif Sadjidine OMBOTIMBE',
    'website': "https://www.sigem.pro",
    "license": "AGPL-3",
    'category': 'Insurance',
    'sequence': -100,
    'version': '15.0.1.0.0',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'data/insured_sequence.xml',
        'views/insured_view.xml',
    ],
    'installable': True,
    'application': True,

}
