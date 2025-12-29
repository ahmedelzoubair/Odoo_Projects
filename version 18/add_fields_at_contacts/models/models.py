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

    delivery_start_hour = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
         ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
        string='Start Hour'
    )

    delivery_start_minute = fields.Selection(
        [('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')],
        string='Start Minute'
    )

    delivery_start_period = fields.Selection(
        [('AM', 'AM'), ('PM', 'PM')],
        string='Start Period'
    )

    delivery_start_time = fields.Char(
        string='Delivery Start Time',
        compute='_compute_delivery_times',
        store=True
    )

    # Delivery End Time fields
    delivery_end_hour = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
         ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
         ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12')],
        string='End Hour'
    )

    delivery_end_minute = fields.Selection(
        [('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')],
        string='End Minute'
    )

    delivery_end_period = fields.Selection(
        [('AM', 'AM'), ('PM', 'PM')],
        string='End Period'
    )

    delivery_end_time = fields.Char(
        string='Delivery End Time',
        compute='_compute_delivery_times',
        store=True
    )

    @api.depends('delivery_start_hour', 'delivery_start_minute', 'delivery_start_period',
                 'delivery_end_hour', 'delivery_end_minute', 'delivery_end_period')
    def _compute_delivery_times(self):
        for record in self:
            # Compute Start Time
            if record.delivery_start_hour and record.delivery_start_minute and record.delivery_start_period:
                record.delivery_start_time = f"{record.delivery_start_hour}:{record.delivery_start_minute} {record.delivery_start_period}"
            else:
                record.delivery_start_time = False

            # Compute End Time
            if record.delivery_end_hour and record.delivery_end_minute and record.delivery_end_period:
                record.delivery_end_time = f"{record.delivery_end_hour}:{record.delivery_end_minute} {record.delivery_end_period}"
            else:
                record.delivery_end_time = False