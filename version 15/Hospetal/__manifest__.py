{
    "name": "Hospital",
    "category": "Hospital",
    "sequennce": -10000,
    "description": "My 1st addon",
    "author": "Odoo Metes",
    "data": ['security/ir.model.access.csv',
             'data/patient_tags_data.xml',
             'data/sequence_data_patient.xml',
             # 'data/sequence_data_appointment.xml',
             'wizard/cancel_appointment_wizard_form.xml',
             'wizard/export_relations_view.xml',
             'views/menu.xml',
             'views/view_patient_form.xml',
             'views/view_femail_patient_form.xml',
             'views/view_appointment_form.xml',
             'views/view_tags_patient_form.xml',
             'views/odoo_playground_view.xml',
             'views/res_config_settings_views.xml',
             'views/view_hospital_operation.xml',

             ],
    "application": True,
    "license": 'LGPL-3',
    "depends": ["mail", "product"]
}

