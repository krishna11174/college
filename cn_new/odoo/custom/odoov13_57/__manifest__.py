# -*- coding: utf-8 -*-
{
    'name': 'COGS Report',
    'version': '13.15',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Inventory',
    'description': """
This module generates xlsx reports for COGS	
""",
    'depends': ['stock','odoov13_47','odoov13_56'],

    'data': [
        'wizard/cogs_cockpit_view.xml',
    ],
    'application': False,
    'installable': True,
}
