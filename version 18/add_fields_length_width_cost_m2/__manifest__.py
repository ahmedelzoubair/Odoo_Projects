# -*- coding: utf-8 -*-
{
    'name': "Capstone Point Carpet",

    'summary': "Add fields length width costm2 pricem2",

    'description': """
Add fields length width costm2 pricem2
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Generic Modules/Stock',
    'version': '18.3',

    # any module necessary for this one to work correctly
    'depends': ['base','product','purchase','sale'],

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

