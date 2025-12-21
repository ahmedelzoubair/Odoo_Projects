# -*- coding: utf-8 -*-
{
    'name': "Analytic distribution field at Purchase Agreements",

    'summary': "Add analytic distribution field at Purchase Agreements form that when change analytic distribution field updated all Purchase Orders",

    'description': """
Add analytic distribution field at Purchase Agreements form that when change analytic distribution field updated all Purchase Orders
    """,

    'author': "Capstone Solutions",
    'website': "https://www.capstonesolutions.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','purchase_requisition'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

