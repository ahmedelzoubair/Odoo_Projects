# -*- coding: utf-8 -*-
{
    'name': "Add fields at Purchase Agreements Line",
    'summary': "Add fields at Purchase Agreements Line",
    'description': """
Add fields at Purchase Agreements Line
    """,
    'author': "Capstone Solutions",
    'website': "https://www.capstonesolutions.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    'depends': ['base', 'purchase', 'purchase_requisition'],

    'data': [
        'views/views.xml',
    ],

    'installable': True,
    'application': False,
    'auto_install': False,
}