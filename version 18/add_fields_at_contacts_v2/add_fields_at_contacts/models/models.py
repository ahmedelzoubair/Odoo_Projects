# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError



class addFieldsAtContacts(models.Model):
    _inherit = 'res.partner'


    customer_code = fields.Char(string="Customer Code")
    commercial_customer_name = fields.Char(string="Commercial Customer Name")
    customer_status = fields.Char(string="Customer Status")
    contact_person = fields.Many2one('res.users', string='Contact Person')
    national_id = fields.Integer(string='National ID')
    google_map_link = fields.Char(
        string='Google Map Link',
        help='Enter Google Maps URL or location link'
    )
    annual_activity_anniversary = fields.Date(string='Annual Activity Anniversary')
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender'
    )
    payment_term_id = fields.Many2one('account.payment.term', 'Payment Type',domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    sales_person = fields.Many2one('res.users', string='Sales Person')



    delivery_start_time = fields.Float(string='Delivery Start Time', help='Time in HH:MM format')
    time_am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')],
    )

    delivery_end_time = fields.Float(string='Delivery End Time', help='Time in HH:MM format')
    time2_am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')],
    )

    @api.constrains('delivery_start_time')
    def _check_time_field(self):
        for record in self:
            if record.delivery_start_time < 0 or record.delivery_start_time >= 24:
                raise ValidationError('Time must be between 00:00 and 23:59')

    @api.constrains('delivery_end_time')
    def _check_time_field(self):
        for record in self:
            if record.delivery_end_time < 0 or record.delivery_end_time >= 24:
                raise ValidationError('Time must be between 00:00 and 23:59')