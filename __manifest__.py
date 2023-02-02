# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'SVIST',
    'version': '14.0.0.01',
    'summary': 'SVIST Software',
    'category': 'Hidden',
    'description': """Join our Comunity bright your futher""",
    'sequence' : -100,
    'demo': [],
    'test': [],
    'depends' : ['sale','stock','mail','report_xlsx','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/admission.xml',
        'wizard/creatingadmission.xml',
        'views/student.xml',
        'views/sale.xml',
        'views/stockpicking.xml',
        'views/hod_details.xml',
        'views/fee.xml',
        'views/seq.xml',
        'views/materials.xml',
        'views/saleorder.xml',
        'report/salerp.xml',
        'report/reports.xml',
        'report/student_template.xml',
        'report/student_tem.xml',

    ],
    'installable': True,
    'auto_install': False,
    'application' : True,
    'license': 'LGPL-3',
}
