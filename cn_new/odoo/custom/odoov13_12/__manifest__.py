{
    'name': 'Odoov13_12_a',
    'version': '13.0.0.11',
    'description': """Delivery Slip Report for Curefit""",
    'category': 'Localization',
    'author': 'Prixgen Tech Solutions Pvt Ltd.',
    'company': 'Prixgen Tech Solutions Pvt Ltd.',
    'website': 'https://www.prixgen.com',
    'depends': ['base','stock','product','web','purchase_stock'],
    'data': [
        'reports/delivery_slip_report.xml',
        'views/delivery_slip_template.xml',
        'views/delivery_slip_views.xml',
        'views/contact_info.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
