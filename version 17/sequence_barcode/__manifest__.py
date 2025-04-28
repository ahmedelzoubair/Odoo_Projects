# -*- coding: utf-8 -*-
{
    'name': "Barcode Sequence",

    'summary': "Create and add sequence to the barcode filed",

    'description': """
Create and add sequence to the barcode filed
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",
    'category': 'Uncategorized',
    'version': '17.1',
    'depends': ['base','product'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/sequence_barcode.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

