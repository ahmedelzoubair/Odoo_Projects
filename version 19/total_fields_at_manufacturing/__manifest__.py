# -*- coding: utf-8 -*-
{
    'name': 'Total Fields At Manufacturing',

    'summary': 'Add total quantity field for bill of materials components, manufacturing orders to consume and consume',

    'description': """
At Manufacturing model --> Products Menu --> Bills of Materials we add new field named (Total) to calculate product_qty column 
And Manufacturing model --> Operations --> Manufacturing Orders add new field named (Total) to calculate product_uom_qty and quantity columns
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",
    'version': '19.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['mrp'],

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

