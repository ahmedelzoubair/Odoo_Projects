from odoo import models, fields, api


class ResConfigSetting(models.TransientModel): # models.TransientModel:- table will not created at the database (create on the fly)
    _inherit = 'res.config.settings' # res.config.settings:- its the model of configuration

    cancel_days = fields.Integer(string="Cancel Days",config_parameter="Hospetal.cancel_days")
    # config_parameter:- hy5ali (cancel_days:- same filed :D ) saving data at (ir.config_parameter), ir.config_parameter:- This model is used to store key-value pairs that can be accessed and modified to configure the system's behavior.(98)
