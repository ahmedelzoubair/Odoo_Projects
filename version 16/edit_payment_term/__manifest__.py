# -*- coding: utf-8 -*-
{
    'name': "Edit Payment Terms",

    'summary': """
        Create a new filed named partner_ids at account.payment.term model as per this field when create a new invoice the customer will 
        see only Payment Term that selected""",

    'description': """
        Create a new filed named partner_ids at account.payment.term model as per this field when create a new invoice the customer will 
        see only Payment Term that selected..
        At version 16.2 we update the functionality of Payment Terms at sales order model as Payment Terms of invoice
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '16.2',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale'],

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
