from email.policy import default

from odoo import api, fields, models, _


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _rec_name = "operation_name"
    _log_access = False # when created models the model created some fields by defulte like ID, when call this attribute the model will not create (create_uid, create_date, write_uid, and write_date) note:- use only at the normal models
    _order = "sequence,id"

    # at appointment model I create a filed related with this model by Many2one relation (116)
    # this model has no filed named name and attribute _rec_name, so when create a new operation form appointment model will not be created
    doctor_id = fields.Many2one('res.users', string="Doctor")
    operation_name = fields.Char(string="Name")
    sequence = fields.Integer(string='Sequence',default=10)

    # the below method to solve the problem of creation from appointment model
    @api.model
    def name_create(self, name): # name:- is the parameter that save the value that put it at appointment model
        return self.create({'operation_name': name}).name_get()[0]



