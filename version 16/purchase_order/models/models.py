# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class PurchaseOrderSteps(models.Model):
    _inherit = "purchase.order"

    step1 = fields.Datetime(string="Step One ", tracking=True,default=datetime.now())
    step2 = fields.Datetime(string="Step Two", tracking=True)
    step3 = fields.Datetime(string="Step Three", tracking=True)
    step_one_done = fields.Boolean(string="Step One", default=False)
    state = fields.Selection(selection_add=[
        ('step_one', 'Step One'),
        ('step_two', 'Step Two'),
        ('step_three', 'Step Three'),
    ])

    def action_step_one(self):
       for rec in self:
           rec.state = 'step_one'

    def action_step_two(self):
       for rec in self:
           rec.state = 'step_two'

    def action_step_three(self):
       for rec in self:
           rec.state = 'step_three'


    # def action_step_one(self):
    #     # Method to set the state to 'step_one' and mark step_one_done as True
    #     self.write({
    #         'state': 'step_one',
    #         'step_one_done': True
    #     })
    #     return True

    # def button_draft(self):
    #     # Call the parent method to keep existing functionality
    #     res = super(PurchaseOrderSteps, self).button_draft()
    #
    #     # Add custom logic to set state to 'step_one' if needed
    #     if self.step_one_done:
    #         self.write({'state': 'step_one'})
    #
    #     return res
