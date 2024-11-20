from reportlab.lib.randomtext import subjects

from odoo import api, fields, models, _
from odoo.addons.test_impex.tests.test_load import message
from odoo.exceptions import ValidationError
from odoo.tools import subtract
from odoo.tools.populate import compute


# ana hena 3aml tabel 2asagl feh el appointment
class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _description = "Hospital Appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'appoint_id'
    _order = 'id desc'  # to rearrange appointment by id decreased (the last app get at the top)

    patient_id = fields.Many2one('hospital.patient', string="Patient Name", tracking=True, ondelete='restrict')
    # =>  In the database, This refers to the foreign key in the hospital_appointment table that links to the id field in the hospital_patient table. The patient_id column contains the unique identifier (id) of the patient from the hospital_patient table.
    # => ondelete='restrict' :- if there is a patient create an appointment u can`t deleted, ondelete='cascade' :- lo delete el patient el appointments beto3o deleted
    appoint_id = fields.Char(string="Appointment ID",readonly=True)
    appointment_date = fields.Date(string="Appointment Date", tracking=1, default=fields.Date.today)
    # tracking = True, but when make tracking=1 that means if u make so changes at many fields appointment_date will appeared at the 1st line. Note:- by default will be = 100
    gender = fields.Selection(related='patient_id.gender')
    # el related=> da attribute hy3`ayer el feild dah 3ala 3ala 7asb 2ele ba3d (=)
    # el related deh hatshta3`l ma3a (fields.Many2one) 3shan met3arf feh koll fields gowa (hospital.patient) model hygeb gender
    ref = fields.Char(string="Reference", related='patient_id.ref')
    # fe ta7t def (onchange_patient_id) hat3`ayer el field dah 3ala 7asb 2ele gowaha
    prescription = fields.Html(string="Prescription")
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'Hight'),
        ('3', 'Very Hight')])  # => field Selection zay gender (0) = option, (Normal) = value
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
    # func1 = lamda name : f"Hellow {name}" => print(func1("Ahmed"))
    # default=lambda self: self.env.company =>the 1st self related to the current model and  (self.env.company) return the id of company that related (res.company(1,)), so the previous  means that i will get the id of the company and add at the company_id field that related to  the current model.
    currency_id = fields.Many2one('res.currency',related='company_id.currency_id')
    # To get currency_id (id lel 3omla) will make relation with res.currency (model that contains all currencies) and then return currency that related to company id

    # deff between (related='patient_id.gender') we (def onchange_patient_id) Use related fields when you want simple synchronization with no additional logic.
    # 2nma (@api.onchange) when you need real-time logic, computation, or interactions with other fields in the same form.
    # @api.onchange('patient_id')
    # def onchange_patient_id(self):
    #     self.ref=self.patient_id.ref
    #     # self.tag_id=self.patient_id.tags_ids

    patient_image = fields.Image(string="Image", related='patient_id.image')
    patient_age = fields.Integer(string="age", related='patient_id.age',store=True)

 # The below (create and write) methods related to methods actually in the system and i will inherited and add anther Functionality.
    # (for more information about those methods return patient model)
    @api.model
    def create(self, vals):
        # super(HospitalAppointment, self).create(vals)
        # vals['appoint_id']= "OMTEST"
        vals['appoint_id'] = self.env['ir.sequence'].next_by_code('appointment.sequence')
        if not self.patient_id and not vals.get('patient_id'):
            raise ValidationError(_("Please select a paitent."))
        return super(HospitalAppointment, self).create(vals)

    # The below method for add more function at the delete button
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
        if not self.patient_id and not vals.get('patient_id'):
            raise ValidationError(_("Please select a paitent."))
        return super(HospitalAppointment, self).write(vals)

    # The below method related to progress field
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

    # The below method related to the button that will change the state of the appointment to in consultation
    def action_in_consultation(self):
        for record in self:
            if record.state == 'draft':
                record.state = 'in_consultation'  # at this step if appointment at any state will change to in cons at draft only

    # The below method related to the button that will change the state of the appointment done
    def action_donee(self):
        for record in self:
            record.state = 'done'
            # after state change to done the below return will get rainbow man with msg Done :D
            return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Done',
                    'type': 'rainbow_man',
                }
            }

    # ana 3amle create lel cancel bass mesh zahro fe Status Bar when click on button

    # The below method related to the button that will open popup wizerd form that related to cancel appointemnt
    def action_cancel(self):
        action = self.env.ref('Hospetal.action_cancel_appointment').read()[0]
        return action
    # Note: at state i create the cancel button but not appered it at the view, so when change the appoinmtent to call the button that named cancel will appears

    # The below method related to the button that will response to direct to Patient but at tree view (the paitent that related to the appointe will appears only)
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

    # The below def for send msg to patient whatsapp num (37 Odoo Whatsapp Integration )
    def action_go_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("Missing phone number"))
        msg = 'Hi *%s* , your *appointment* number is: %s ,Thanks' % (self.patient_id.name,self.appoint_id)
        whatsapp_api_url = 'https://api.whatsapp.com/send?phone=%s&text=%s' % (self.patient_id.phone,msg)
        # phone=%s:- the meaning of (%) is will getting replaced by self.patient_id.phone
        # phone=%s&text=%s:- if we have multi values must replace the data by tubel
        self.message_post(body=msg, subject='Whatsapp Message')
        # message_post:- will add the msg and subject to the oe_chatter when click at whatsapp button, Note: must keep msg variable to get it at the chatter
        return {
            'type': 'ir.actions.act_url',
            'url': whatsapp_api_url,
            'target': 'new',
        }

    # The below method that add to notification button which make two functions show notification and open form view of the patient (Display Notification in odoo (157))
    def action_notification(self):
        message = "Button click successful !!"
        action = self.env.ref('Hospetal.action_hospital_patient')
        # action:- I get the action of the patient view form from : depuger => Edit Action => External ID, cuz action does not include the model name
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',

            'params': {
                'title': _('Click her to open *%s* with ID (%s)',self.patient_id.name,self.patient_id.id),
                # title:- msg will appears  for appears the message remove title
                'message': '%s',
                # Note:- if i remove links and put the previous message variable i will get only the msg
                'type': 'success',
                # type': 'success' :- make the notification with a blue color, Note:- warming = orange, danger = red
                'sticky': False,
                # 'sticky': False :- the notification will disappear after few sec
                'links': [{
                # links:- for add link when clicked open the below
                    'label':self.patient_id.name,
                    # 'label':- which field at patient will appears at the notification
                    'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient&view_type=form&view_mode=form',
                    # action={action.id}:- will target the id of the related action
                    # id={self.patient_id.id}:- which id will target (self.patient_id)
                    # model=hospital.patient:- target the model
                    # 'view_type=form' and 'view_mode=form' ensure the form view opens
                    # ------ To open the tree view of all patients check the below url
                    # 'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient',
                }],
                # The below will open the patient form like smart buttons (at the same page and Gives authority go previous page)
                'next':{
                    'type': 'ir.actions.act_window',
                    'res_model' : 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False,'form')]
                }
            }
        }