# -*- coding: utf-8 -*-
{
    'name': "PO-Approvals",
    'version': '0.4',
    'summary': """
        Dynamic Approval Management Application""",
    'sequence': 4,

    'description': """
        Every purchase order can have multiple approvals  through this application
    """,

    'author': "Prime Minds Consulting Pvt.Ltd",
    'website': "http://primeminds.co",
    'depends': ['base', 'purchase', 'sale', 'purchase_requisition', 'product', 'analytic'],
    'auto_install': False,
    'installable': True,
    'application': True,
    'data': [
        'security/po_approval_group.xml',
        'security/ir.model.access.csv',
        'views/po_approval.xml',
        'views/company_data.xml',
        'views/vendor_pricelist.xml',
        # 'reports/purchase_edit_report.xml',
    ],

    'demo': [
    ],
}
