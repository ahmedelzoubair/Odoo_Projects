# -*- coding: utf-8 -*-
{
    'name': "Capstone Confirmation Authority",

    'summary': """Confirmation authority with a checkbox in user setting """,

    'description': """
        Confirmation authority with a checkbox in user setting to allow specific users to be able to confirm the order
    """,

    'author': "Cap-stone Solutions",
    'website': "https://www.capstone-solution.com",

    # Categories can be used to filter modules in modules listing
    # for the full list
    'category': 'Uncategorized',
    'version': '18.0.0.2',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'security/groups.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
