# -*- coding: utf-8 -*-
{
    'name': "Apply Button Access Right",

    'summary': """
        This model is adding inventory tab in the category inventory in setting (Can Apply Inventory Adjustment) 
        to show and hide the apply button in inventory adjustment""",

    'description': """
        This model is adding inventory tab in the category inventory in setting (Can Apply Inventory Adjustment) 
        to show and hide the apply button in inventory adjustment
    """,

    'author': "Capstone Solutions",
    'website': "https://www.capstonesolutions.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'security/group.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
