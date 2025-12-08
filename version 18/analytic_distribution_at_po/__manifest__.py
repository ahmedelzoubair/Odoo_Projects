# -*- coding: utf-8 -*-
{
    'name': "Analytic distribution field at PO",

    'summary': "Add analytic distribution field at PO form that when change analytic distribution field at Lines updated",

    'description': """
Add analytic distribution field at PO form that when change analytic distribution field at Lines updated
    """,

    'author': "Capstone Solutions",
    'website': "https://www.capstonesolutions.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase'],

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

