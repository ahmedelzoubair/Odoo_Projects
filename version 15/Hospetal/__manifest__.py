{
    "name": "Hospital",
    "category": "Hospital",
    "sequennce": -10000,
    "description": "My 1st addon",
    "author": "Odoo Metes",
    "data": ['security/ir.model.access.csv',
             'data/patient_tags_data.xml',
             'data/decimal_accuracy.xml',
             'data/sequence_data_patient.xml',
             # 'data/sequence_data_appointment.xml',
             'wizard/cancel_appointment_wizard_form.xml',
             'views/menu.xml',
             'views/view_patient_form.xml',
             'views/view_femail_patient_form.xml',
             'views/view_appointment_form.xml',
             'views/view_tags_patient_form.xml',
             'views/odoo_playground_view.xml',
             'views/res_config_settings_views.xml',
             'views/view_hospital_operation.xml',
             'report/report.xml',
             'report/patient_card.xml',
             'report/appointment_medicine_lines.xml',
             'report/cancel_appointment_wizard.xml',

             ],
    "application": True,
    "license": 'LGPL-3',
    "depends": ["mail", "product","report_xlsx"]
}

