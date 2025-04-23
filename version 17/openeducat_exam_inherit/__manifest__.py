# -*- coding: utf-8 -*-
{
    'name': "Additional Degree",

    'summary': "Add new fields at Exam page and Result Lines",

    'description': """
Add new field named maximum_additional_degree at Exam page and additional_degree, additional_degree fields at Result Lines
    """,

    'author': "Cap-Stone Solutions",
    'website': "https://www.capstone-solution.com",
    'category': 'Uncategorized',
    'version': '17.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'openeducat_exam'],

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

