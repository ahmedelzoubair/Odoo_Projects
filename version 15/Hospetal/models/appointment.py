from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools.populate import compute


# ana hena 3aml tabel 2asagl feh el appointment
class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'appoint_id'
    # 3shan lama 2ft7 any appointment yegele fo2 2sm el patient bata3 el appointment de mesh rakm e creation el appointment fe data base
    _order = 'id desc'  # tarteb el app fe el <tree> view hab2ba 2a5r app get to the top

    patient_id = fields.Many2one('hospital.patient', string="Patient Name", tracking=True, ondelete='restrict')
    # =>  In the database, This refers to the foreign key in the hospital_appointment table that links to the id field in the hospital_patient table. The patient_id column contains the unique identifier (id) of the patient from the hospital_patient table.
    # => ondelete='restrict' :- if there is a patient create and an appointment u can`t deleted, ondelete='cascade' :- lo delete el patient el appointments beto3o deleted
    appoint_id = fields.Char(string="Appointment ID")
    appointment_date = fields.Date(string="Appointment Date", tracking=1, default=fields.Date.today)
    # if tracking=1 that means appointment_date to get the 1st Always a priority, Note:- by defulte will be = 100
    gender = fields.Selection(related='patient_id.gender')
    # el related=> da attribute hy3`ayer el feild dah 3ala 3ala 7asb 2ele ba3d (=)
    # el related deh hatshta3`l ma3a (fields.Many2one) 3shan met3arf feh koll fields gowa (hospital.patient) model hygeb gender
    ref = fields.Char(string="Refrence", related='patient_id.ref')
    # fe ta7t def (onchange_patient_id) hat3`ayer el field dah 3ala 7asb 2ele gowaha
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'Hight'),
        ('3', 'Very Hight'),
    ])  # => field selction zay gender (0) = option, (Normal) = value
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel')], required=True, default='draft', tracking=True, string="Status Bar")
    active = fields.Boolean(string="Active", default=True)
    doctor_id = fields.Many2one('res.users', state="Doctors",tracking=True)
    # field related ma3a moduel res.users bygeb el name by defould Note:- for Many2one avatar and user widget -41-
    appointment_pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id')
    #  de relation One2many that means 2en el one appointment feha 2akter men line
    #  'appointment_id' => fe el module appointment.pharmacy.lines hatla2e feh filed Many2one dah 2smo (49)
    hide_seals_price = fields.Boolean(string="Hide Seals Price")
    tag_id = fields.Many2many(string="Patient Tags", related='patient_id.tags_ids')
    operation = fields.Many2one('hospital.operation', string="Operation")
    progress = fields.Integer(string="Progress", compute="_compute_prescription")
    duration = fields.Float(string="Duration Days",tracking=True)
    # dah field wa5d fe xml at calender rec tage (date_delay) 3shan lama 23ml expand le appointment (ya3ni lo app hata5od 2kter men youm)

    # the below fields to add field price_subtotal to calculate the total price (quantity * price) as total at sales order (Monetary Field And Widget Monetary 132)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    # 1st get the company id of the Current appointment:- we make relation Many2one with model that save all the companies to get the company that created this appointment
    # default=lambda self: self.env.company:- lambda fun to get (self.env.company)  company id of the Current appointment
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id')
    # I get currency_id (id lel 3omla) that related to the company_id that this appointment created in

    # deff between (related='patient_id.gender') we (def onchange_patient_id) Use related fields when you want simple synchronization with no additional logic.
    # 2nma (@api.onchange) when you need real-time logic, computation, or interactions with other fields in the same form.
    # @api.onchange('patient_id')
    # def onchange_patient_id(self):
    #     self.ref=self.patient_id.ref
    #     # self.tag_id=self.patient_id.tags_ids

    def action_in_consultation(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'in_consultation'  # at this step if appointment at any state will change to in cons at draft only

    def action_done(self):
        for record in self:
            record.state = 'done'
            # after state change to done the below return will get rainbow man we msg Done :D
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Done',
                    'type': 'rainbow_man',
                }
            }

    # ana 3amle create lel cancel bass mesh zahro fe Status Bar when click on button
    # creation of cancel apperd automatic at Status Bar by change self.state='cancel'

    def action_cancel(self):
        action = self.env.ref('Hospetal.action_cancel_appointment').read()[0]
        return action

    def action_go_to_patient(self):
        return {
            'name': _('Go To Patient'),
            'res_model': 'hospital.patient',
            'view_mode': 'list,form',
            'context': {},
            'domain': [('appointment_ids', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }

    # ana 3`ayrt el action def badal makant betzahr zorar el acc
    # ba2t 3mla zay button 2ele type="action" :- 2awel mados 3aleh yfta7lk el form view 2ele marbota be action dah (64)

    @api.depends('state')
    def _compute_prescription(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = 25
            elif rec.state == 'in_consultation':
                rec.progress = 50
            elif rec.state == 'done':
                rec.progress = 100
            else:
                rec.progress = 0

    @api.model
    def create(self, vals):
        # super(HospitalAppointment, self).create(vals)
        # vals['appoint_id']= "OMTEST"
        vals['appoint_id'] = self.env['ir.sequence'].next_by_code('appointment.sequence')
        return super(HospitalAppointment, self).create(vals)

    # el method 2ele ta7t 3shan 2azawed option 3ala button delete 2ele gowa action
    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can delete only (Draft) appointment"))
        return super(HospitalAppointment, self).unlink()

    # If you remove the super() call, your method would completely replace the parent method,
    # and the original deletion logic in the parent class would not be executed.
    # This would mean that your record wouldn't actually be deleted,
    # because you've overridden the unlink method without carrying out the actual deletion.

    def write(self,vals):  # => de method for (Edit) button, (vals) hena hatrage el fields 2ele 3amlt 3alehon edit mesh kolo
        # => ta2dreben koll ma create model beya5od func (create and edit) auto fa 2awel mat3ml fuc same name and parameters be inhert same func + new func
        if not self.appoint_id and not vals.get('appoint_id'):  # => lo 3amlt edite we ref fade 7a22 el line 2ele ta7t
            vals['appoint_id'] = self.env['ir.sequence'].next_by_code('appointment.sequence')
        return super(HospitalAppointment, self).write(vals)

    # the below def to make a button open a link web site (URL) (134:- URL Action In Odoo || Redirect To URL From Code || Odoo URL Actions)
    def action_test_url(self):
        return {
            'type': 'ir.actions.act_url',
            'url': 'https://www.google.com/',
            # 'url': self.prescription,
            # 'url': 'https://localhost:8015/shop', => if u create at website model page name shop will open it
            'target': 'new',
        #   'target': "self" => will open googel at the same page of odoo

        }

    # the below def for send msg to patient whatsapp num (37 Odoo Whatsapp Integration )
    def action_go_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("Missing phone number"))
        msg = 'Hi *%s* , your *appointment* number is: %s ,Thanks' % (self.patient_id.name,self.appoint_id)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone,msg)
        # phone=%s:- the meaning of (%) is will getting replaced by self.patient_id.phone
        # phone=%s&text=%s:- if we have multi values must replace the data by tubel
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_api_url,
            'target': 'new',
        }