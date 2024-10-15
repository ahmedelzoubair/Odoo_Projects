from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


# ana hena ha3ml tabel bass mesh haytsagl fe data base (create on the fly)
class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    # el func de el default we 2ana override 3aleha 3shan 2t7akm 2aktr fe default value
    @api.model
    def default_get(self,fields): # => el default func bett3arf 2abl variables 3shan teda5l fehm el data badal el vals fileds (78)
        res = super(CancelAppointment,self).default_get(fields) # => 3amlt run lel func (CancelAppointment) 3shan get variables
        res['date_cancel'] = date.today()
        if self.env.context.get('active_id'): # => If 'active_id' exists, it returns the value (the ID); if not, it returns None.
            res['appointment_id'] = self.env.context.get('active_id') # => 5ali el active_id = _rec_name of appointment_id
        return res
    # hena ana momkn add le date_cancel default value bit appointment_id 2afdl tare2a leh hena code 2ele fo2 2o
    # NOTE:- 1) fe 2e 7all men el 27wal el date_cancel = today date why no conditions
    #   2) appointment_id mesh hayeege fe data 2ela lo 2ana fat7 appointment 3shan 2akon sa7b id (appointment_id) 2nma lo fe tree mafesh id so mafesh appointment_id
    #   3) reason mesh haytketb fe 7aga 2ela lama 2ados 3ala button 2ele gowa appointment model 3shan howa dah el makan 2ele mesagel feh context="{'default_reason': 'text from appointment form by default_reason'}



    appointment_id = fields.Many2one('hospital.appointment', string="Appointment ID",
                                     domain=['|',('state','=','draft'),('priority','in',('1','2',False))])
    # el field dah bygeb koll appointment 2ele gowa model appointment Note: [don`t forget 2en el models de 3obara 3an databases fa .Many2one beya5od el primary key of (appointment) and put it as foreign key at (cancel_appointment)]
    # domain => is attribute bet5ali fe (condition) lel appointment 2ele hatege mesh hatgeb koll appointments
    # ('state','=','draft') => (state) fields.Selection field in appointment feh stafe appointment (draft wala done wala cancel,...)
    # ('priority','in',('1','2',False) => priority fields.Selection field in appointment feh stars of appointment
    # ma3naa koll line => 2ene 2ageb el appointment el draft or ('|',) wa5da 1 2o 2 2o mesh wa5da wala satar

    reason = fields.Text(string="Reason")
    # dah feild zay el char bass koll matktb 2kter ykber ma3ak (63)
    date_cancel = fields.Date(string="Cancelation Date")

    def action_cancel(self): #zorar cancel 2ele fe cancel appointemnt lo date of app = todays date raise error
        cancel_days = self.env['ir.config_parameter'].get_param('Hospetal.cancel_days') # ir.config_parameter:- dah el model 2ele beytsagl gwah filed 2ele betshel data gowa settings (114)
        allowed_days = date.today() - relativedelta.relativedelta(days=int(cancel_days))
        # if self.appointment_id.appointment_date == fields.Date.today(): #dah bageb meno tare5 el nahrda /// # note:- field of appointment_date lazm yekon no3o date 3shan fields.Date tshta3`al 3aleh lo DateTime bye bye kambora
        if self.appointment_id.appointment_date > allowed_days: #dah bageb meno tare5 el nahrda /// # note:- field of appointment_date lazm yekon no3o date 3shan fields.Date tshta3`al 3aleh lo DateTime bye bye kambora
            # appointment_id.appointment_date = 10/sep/2024 > allowed_days = 7/sep/2024 (date.today(12/sep/2024) - 5)
            raise ValidationError(_(f"To cancel appointment must it is repeated on it {allowed_days} days "))
        else:
            self.appointment_id.state = 'cancel'
        return { # el return de hat5ali lama press cancel button page reloaded 
            'type':'ir.actions.client', #This tells Odoo that the action is client-side, meaning it will be handled by JavaScript running in the browser rather than by typical server-side logic.
            'tag':'reload'
        }

