# -*- coding: utf-8 -*-
{
    'name': "Barcode Field In Operations",

    'summary': "This model is adding a Barcode field in operations transfers",

    'description': """
Create a new field at stock.move model named barcode_product to reflect the data of barcode field at product to operations transfers.
    """,

    'author': "Capstone Solutions",
    'website': "https://www.capstonesolutions.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    'depends': ['base','stock'],
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

