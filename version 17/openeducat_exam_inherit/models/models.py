
from odoo import models, fields, api,_
from odoo.exceptions import ValidationError


class openeducatexaminherit(models.Model):
    _inherit = "op.exam"

    maximum_additional_degree = fields.Integer(string="Maximum Additional Degree")


class opresultlineinherit(models.Model):
    _inherit = ['op.result.line']

    exam_id = fields.Many2one("op.exam")
    maximum_additional_degree = fields.Integer(string="Maximum Additional Degree",related="exam_id.maximum_additional_degree")

    additional_degree = fields.Integer(string="Additional Degree")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submit', 'Submit'),
        ('approved', 'Approved')], string="Status Bar",default='draft')


    def action_submit(self):
        for record in self:
            if record.additional_degree > record.maximum_additional_degree:
                raise ValidationError(_("Not Accepted, Because Additional Degree greater than Maximum Additional Degree "))
            else:
                record.state = 'submit'

    def action_approved(self):
        for record in self:
            record.marks = record.marks + record.additional_degree
            record.state = 'approved'

    def action_reset_to_draft(self):
        for record in self:
            record.state = 'draft'
