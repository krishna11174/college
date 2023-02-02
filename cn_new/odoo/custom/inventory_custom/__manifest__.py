# -*- coding: utf-8 -*-
{
    'name': "Inventory Custom",
    'version': '0.4',
    'summary': """
       Inventory Customisation Application""",
    'sequence': 4,

    'description': """
        Inventory Customisation Application for inventory adjustment matrix
    """,

    'author': "Prime Minds Consulting Pvt.Ltd",
    'website': "http://primeminds.co",
    'depends': ['base', 'purchase', 'sale', 'stock', 'product', 'analytic',
                'odoov13_9','odoov13_34'],
    'auto_install': False,
    'installable': True,
    'application': True,
    'data': [
        'security/inventory_approval_group.xml',
        'security/ir.model.access.csv',
        'views/inventory_custom.xml',
        'views/grn_po.xml',
        'views/purchase_product.xml',
        'views/inventory_report.xml',
        'views/grn_alert.xml',
        'wizard/shelflife_wizard.xml',
        'views/product_custom.xml',
    ],

    'demo': [
    ],
}
