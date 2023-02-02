{
    'name': 'Odoov13_20a',
    'version': '13.0.0.2',
    'category': 'Inventory',
    'author': 'Prixgen Tech Solutions Pvt Ltd.',
    'company': 'Prixgen Tech Solutions Pvt Ltd.',
    'website': 'https://www.prixgen.com',
    'summary': 'There is an extra field added in STO screen to capture the done qty of respective delivery orders',
    'depends': ['stock','odoov13_19'],
    'data': [
        'views/stofields.xml',
        
        # 'security/ir.model.access.csv',
        #'views/purchase_order_view.xml',
        #'views/stock_picking.xml',
        #'views/purchase_order_web.xml',
        
    ],
    'qweb': [

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
