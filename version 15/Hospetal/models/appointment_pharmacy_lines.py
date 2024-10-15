from odoo import api, fields, models
from datetime import date


# ana hena 3aml tabel 2asagl feh el dawa2 2ele hay5do el patient @ the appointment
class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity",default=1)
    price = fields.Float(string="Sales Price",related='product_id.list_price')
    appointment_id = fields.Many2one('hospital.appointment')
    appointment_datee = fields.Date(string="Appointment Date",related="appointment_id.appointment_date")

    currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    # field related to model that content all currencies (3omlate) bass related (mabni 3ala) relation between
    # (appointment.pharmacy.lines) and hospital.appointment to get currency_id that at the created appointment
    price_subtotal = fields.Monetary(string="Subtotal",compute="_compute_price_subtotal")
    # this field to (price * quantity), Monetary:- to get currency that related to appointment company
    # Note:- if change name of currency_id need the below, cuz (currency_id) met3arf at system by default but any anther name must add at price_subtotal field attribute to ye3arf company_currency_id
    # company_currency_id = fields.Many2one('res.currency', related='appointment_id.currency_id')
    # price_subtotal = fields.Monetary(string="Subtotal",compute="_compute_price_subtotal",currency_field='company_currency_id')

    # the below def to _compute_price_subtotal :D
    @api.depends('price','quantity')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal = rec.price * rec.quantity
