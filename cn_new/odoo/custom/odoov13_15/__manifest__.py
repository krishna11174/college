
{
    'name': 'Odoov13_15a',
    'summary': """Material Requisition Creation""",
    'description': """For Curefit, a Material Request is created manually and no dependency of Analytic Account or mrp""",
    'version': '13.0.2.12',
    'author': "Prixgen Tech Solutions Pvt. Ltd.",
    'website': 'https://www.prixgen.com',
    'company': 'Prixgen Tech Solutions Pvt. Ltd.',
    'category': 'Inventory',
    'depends': ['stock','base','odoov13_4','curefit_api_integration_patch'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'security/config_settings.xml',
        'views/inventory_indent.xml',
        'views/mrp_indent.xml',
        'views/mrp_indent_active.xml',
        'views/stock_picking_views.xml',
        # 'views/scrap_order.xml',
        'data/ir_sequence_data.xml',
        # 'views/indent_date.xml',
        # 'views/manufacturing_plan_view.xml',
        # 'views/res_config_settings.xml',
    ],
    'installable': True,
    'auto_install': False,
}