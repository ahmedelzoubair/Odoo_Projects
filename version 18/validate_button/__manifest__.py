# -*- coding: utf-8 -*-
{
    'name': "Scrap Validate Button",

    'summary': "At users we create new Access Right to determine who can use Scrap Validate Button",

    'description': """
At users we create new Access Right to determine who can use Scrap Validate Button
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",
    'category': 'Uncategorized',
    'version': '18.0.1.0.0',
    'depends': ['base','stock'],

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
