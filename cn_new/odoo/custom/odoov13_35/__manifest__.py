# -*- coding: utf-8 -*-
{
    'name': 'MR Report',
    'version': '13.0.0.9',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'company':'Prixgen Tech Solutions Pvt. Ltd.',
    'website': "https://www.prixgen.com",
    'category': 'Inventory',
    'orign': 'Project Specific',
    'description': """
This module generates xlsx reports for MR	
""",
    'author': "Prixgen tech Solutions",
    'depends': ['stock','odoov13_15'],
    'external_dependencies': {"python" : ["openpyxl"]},
    'data': [
        'wizard/mr_report_view.xml',
    ],
    'application': False,
    'installable': True,
}
