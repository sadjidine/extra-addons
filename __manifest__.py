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
     HIRMS module which is used to manage healthcare insurance systems activities 
     and records.
    """,
    'author': "Salif Sadjidine OMBOTIMBE",
    'company': "SIGEM",
    'maintainer': 'Salif Sadjidine OMBOTIMBE',
    'website': "https://www.sigem.pro",
    "license": "AGPL-3",
    'category': 'Insurance',
    'sequence': -100,
    'version': '15.0.1.0.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'security/hirms_security.xml',
        'data/insured_sequence.xml',
        'views/company.xml',
        'views/district.xml',
        'views/department.xml',
        'views/locality.xml',
        'views/category.xml',
        'views/speciality.xml',
        'views/codification.xml',
        'views/nomenclature.xml',
        'views/pathology.xml',
        'views/medication.xml',
        'views/molecule.xml',
        'views/medication_form.xml',
        'views/therapeutic_route.xml',
        'views/policy.xml',
        'views/hirms_menu.xml',
        'views/insured_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
