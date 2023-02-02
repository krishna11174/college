# -*- coding: utf-8 -*-
{
    'name': 'Odoov13_11a',
    'version': '13.0.1.0',
    'category': 'Customization',
    'description': u"""
This model aggrigates inventory
""",
	'author': 'Prixgen Tech Solutions Pvt Ltd',
    'depends': [
        'base',
        'product',
        'stock',
        'odoov13_4'
    ],
    'data': [
        'views/views.xml',
        # 'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
