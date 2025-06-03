# -*- coding: utf-8 -*-
{
    'name': "Change Analytic Account Automatically",

    'summary': "At purchase model when change analytic account field at 1st order line all the rest order lines take the same analytic distribution automatically",

    'description': """
    At purchase model when change analytic account field at 1st order line all the rest order lines take the same analytic distribution automatically
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Purchase',
    'version': '18.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

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

