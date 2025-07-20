# -*- coding: utf-8 -*-
{
    'name': "Update Delivery Slip Report",

    'summary': "Remove report column from Delivery Slip Report ",

    'description': """
Remove report column from Delivery Slip Report
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",
    'category': 'Generic Modules/Stock',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'report/delivery_slip.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

