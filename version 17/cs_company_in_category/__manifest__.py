# -*- coding: utf-8 -*-
{
    'name': "Filter Product Category Based On Company",
    'summary': "This model adding company field in product category",
    'description': """This model adding company field in product category""",
    'author': "Eng Abdulrahim: Capstone Solutions",
    'website': "https://www.capstone-solution.com",
    'category': 'Uncategorized',
    'version': '17.0.0.1',
    'depends': ['base', 'product'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
