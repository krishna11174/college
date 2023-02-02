# -*- coding: utf-8 -*-
{
    'name': 'Purchase Receipt Date',
    'version': '13.0.0.10',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'App origin':'Project Specific',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'license': 'OPL-1',
    'category': 'Tools',
    'summary': 'Purchase Receipt Date',
    'description': """
Purchase Receipt Date
---------------------

Purchase Receipt Date
""",
    'depends': ['odoov13_50','purchase', 'stock','purchase_stock'],
    'data': [
        'views/origin_product.xml',
        'views/views.xml',
    ],
    'installable': True,
    'auto_install': False,
}
