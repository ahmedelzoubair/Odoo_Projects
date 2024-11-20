from email.policy import default
from re import search

from dateutil.utils import today

from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta

from odoo.tools.populate import compute


# ana hena 3aml tabel 2asagl feh el patient
class HospitalPatients(models.Model):
    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # 'mail.thread' :- responsible to bring the tracking fields
    # _rec_name = 'name'

    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    name = fields.Char(string="Name", tracking=True, required=True)
    date_of_birth = fields.Date(string="Patient Birth Day")
    age = fields.Integer(compute='_compute_age', inverse="_inverse_compute_age", store=True,tracking=True)  # note:- the compute filed do not store by default database
    # inverse="_inverse_compute_age":- de def 3shan lama add el age date yet7sb automatic (99)
    # search='_search_age':- 3shan compute field not stor at database so when search by age nothing done so i will make this search def (100)
    active = fields.Boolean(string="Active", default=True)
    ref = fields.Char(string="Reference", readonly=True)
    image = fields.Image(string="Image")
    appointment_count = fields.Integer(string="Appointment Numbers", compute='_compute_appointment_count',store=True)  # => store=True:- compute filed will save at Database
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    tags_ids = fields.Many2many('patients.tags', string="Tags")
    # da field related ma3a (patients.tags) module to create tags, ana keda 3aml table 3rd rabet beh tages be patients (57)
    parent = fields.Char(string="Parent Name")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status",trace=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Is Birthday", compute='_compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    # this method that responsible for create function at odoo, take parameters (self,vals)
    @api.model  # => 3shan 2awsl le methode ll (create) lazm 2aro7 le dictionary (api) gowa (model) (71)
    def create(self,vals):  # => this method that responsible for create function at odoo, take parameters (self,vals), (self) related to object will created form class, (vals) vals:- is the dictionary that contains the initial values that are used to create the new record, holding the field data that will be stored in the database.
        # super(HospitalPatients, self).create(vals) => (super) that means I will override the main class with the below function
        # vals['ref']= "OMTEST" => get the 'ref' attribute add in it value
        vals['ref'] = self.env['ir.sequence'].next_by_code('patient.sequence')  # => self.env['ir.sequence']:- call env od model ir.sequence ('ir.sequence'):- model 2ele feh koll sequ beta3t sys, (next_by_code):- methoud mas2ola 3an sequ,(patient.sequence):- index beta3 sequ patient (72)
        return super(HospitalPatients, self).create(vals)  # return main create function and add to her functionality (make ref=OMTEST)
        # Note: if I call super first  

    # this methode that responsible for Edite function at odoo, take parameters (self,vals)
    def write(self,vals):  # => de method for (Edit) button, (vals) hena hatrage el fields 2ele 3amlt 3alehon edit mesh kolo
        # => ta2dreben koll ma create model beya5od func (create and edit) auto fa 2awel mat3ml fuc same name and parameters be inhert same func + new func
        if not self.ref and not vals.get('ref'):  # => lo 3amlt edite we ref fade 7a22 el line 2ele ta7t
            vals['ref'] = self.env['ir.sequence'].next_by_code('patient.sequence')
        if 'gender' in vals:
            # If gender is being set, ensure it's not empty
            if not vals.get('gender'):
                raise ValidationError(_("Please select a valid gender."))
        else:
            # If gender is not being updated, ensure the record already has a gender
            if not self.gender:
                raise ValidationError(_("Please select a gender before saving."))
        return super(HospitalPatients, self).write(vals)

    # 3shan 23del fe (_rec_name) 2a5aleh ta5od more than one variable
    def name_get(self):
        # result = []
        # for record in self:
        #     name = record.ref + "/" + record.name
        #     result.append((record.id, name))
        # return result
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]  # (75)

    # el def 2ele ta7t 3shan add conditeon 3ala button el delete
    @api.ondelete(at_uninstall=False)  # @api.ondelete:- decorator to add option to button delete, (at_uninstall=False):- ya3ni lo model ma3mlo uninstall el def 2ele ta7t mesh hatsta3`al lo 3amlt (=True) the method would be executed even during the uninstallation of the module
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("Can not delete this patient because has appointment "))

    @api.constrains('date_of_birth')  # => 3shan add condtion (shart) 3ala filed "date_of_birth" (83) constrains [Used for validation,Raises errors if constraints are violated,Prevents records from being saved if validation fails.]
    def _check_date_of_birth(self):  # => (_check_) tare2t ketaba (date_of_birth) el filed 2ele hay2sl 3aleh constrains
        for rec in self:
            if rec.date_of_birth >= fields.Date.today():  # => lo add date ba3d today date el (_compute_age) func hat7sb el date by -ve value
                raise ValidationError(_("The Date That You Add Is Not Acceptable"))

    @api.depends('date_of_birth')  # => 3shan el filed teg3`ar men 3`ar save () depends[Used for computed fields,Automatically recalculates the values of fields that depend on the specified fields, Does not raise validation errors, just recalculates the field's value.]
    def _compute_age(self):  # => self 3aeda 3ala object of the class (patient)
        for rec in self:  # => for 3shan el self hygrb koll attributs 2ele fo2
            today = date.today()  # => tare5 el naharda
            if rec.date_of_birth:  # => 2awel ma self (rec) tegeb date_of_birth nafz 2ele ta7t
                rec.age = today.year - rec.date_of_birth.year  # => 5ale age = tare5 el nahrda - tare5 el patient
            else:
                rec.age = 0  # => 3shan lo patient birth day empety no error

    @api.onchange('age')  # when change at age filed execute the below code (99)
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
            # relativedelta is part of the dateutil library and is used to perform relative date calculations. It allows you to add or subtract specific time periods, such as years, months, days, etc.
            # years=rec.age means that the relative delta is calculated based on the age of the record (rec.age), which is assumed to be an integer representing the person's age in years.
            # For example, if today's date is 2024-09-02 and rec.age is 25, it calculates the date_of_birth by subtracting 25 years from today's date.

    def _search_age(self, operator,value):  # this how to create search fun must add operator and value (value:- the int number add by user then search with it by age) parameter (100)
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)  # field (date_of_birth) = (tare5 el nahrda - tare5 el value add by cust) for ex:- if value today = 10/9/2024 , value = 24 ( relativedelta.relativedelta(years=value) = 24 ) then date_of_birth = 10/9/2020
        # return [('date_of_birth','=',date_of_birth)] # el return de hatgeb koll mawaled 2020 {bass} just [10/9] not all in 2020 so this return not work
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]
        # date_of_birth date filed means it`s same date.today() continue day, month and year
        # start_of_year:- date_of_birth (2020) replace at day (1) month (1)
        # end_of_year:- date_of_birth (2020) replace at day (31) month (12)
        # then this return will get all of people of all the year no like the previous comment return

    @api.depends('appointment_ids')  # =>  appointment_ids:- dah filed one2many ma3a appointment ya3ni one paitent can have alot of appointments falama depends 3alah ya3ni koll app cont el count
    def _compute_appointment_count(self):
        # appointment_group = self.env['hospital.appointment'].read_group(domain=[],fields=[],groupby=[]) => get all elements (num) that related between hospital.patient and hospital.appointment  (128)
        appointment_group = self.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'], groupby=['patient_id'])  # (128) domain=[('state','=','done')] => will get only done app
        # ana 3amlt calling lel method (read.group) [method mas2ola 3ala 2naha t3ml grouping and call all fields by field name "patient_id" ] Note:- men 3`ar el (patient_id) hygebli 3add 2ele el fields 2ele ma3molohem relation
        for app in appointment_group:  # el for de 3shan 2a3adi 3ala koll filed (same of for loop at self)
            # if we print app => {'patient_id_count':9, 'patient_id':(3, <odoo.tools.func.lazy obj>), '__domain':[('patient_id','=',3)]} # patient_id_count:- filed Generated auto from (.read_group) to count elements (num) that related between hospital.patient and hospital.appointment
            patient_id = app.get('patient_id')[0]  # [0]:- to get 1st element at tuble (id) => 3
            patient_rec = self.browse(patient_id)  # .browse() :- method hada5alk gowa modle, patient_id:- el id 2ele gebto men (.read_group), That means i get all the of record of patient id 3 (for exmple) and add it in (patient_rec)
            patient_rec.appointment_count = app.get('patient_id_count')  # after getting all fields of patient with id (3) i will target appointment_count add put in it patient_id_count (9) that created from read_group methode
            self = self - patient_rec
            # 27na fe loop betgeb koll el relation elements between two models, so => main self [hospital.patient(2,3,14,17,50)] = self [hospital.patient(2,3,14,17,50)] - patient_rec [hospital.patient(2,)] de 2awll mara
            # then fe tane mara ba2t el (main self) = [hospital.patient(3,14,17,50)]
            # then el (patient_rec) hatgeb koll relation elements [ma3ada] el elements 2ele mafesh mabenhom relation [hospital.patient(17) and hospital.patient(50)]
            # then final self = hospital.patient(17,50)
        self.appointment_count = 0
        # self = self - patient_rec: Removes the current patient_rec from self. => self.appointment_count (hospital.patient(17,50)) = 0

        # ---------------------------------------------------------------------
        # for rec in self:
        #     rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
        # => self.env['hospital.appointment'] :- calling the env of appointment model
        # => search_count :- method at env to search for numbers of related inherit objects from anther model  ..
        # => [('patient_id','=',rec.id)] :- is the condition of method (filed el relation between two models),
        # patient_id:- dah filed many2one gowa appointment rabt el appointment with patient
        # rec.id:- dah 2l unique filed created by system by default

    # el def de 3shan 2asha3`l smart button:- smart button will open the appointments that related to the patient
    def action_view_appointments(self):
        return{
            'name' : _('Appointments'),
            'res_model' : 'hospital.appointment',
            'view_mode' : 'list,form',
            'context' : {'default_patient_id':self.id},
            # Passing default patient_id via context, The context is being passed when an action is returned. In this case, it ensures that when the user creates a new appointment, the patient_id field is already filled in with the current patient’s ID.
            'domain' : [('patient_id','=',self.id)],
            # Add a condition to the view to open the appointments that related to the patient id of self
            'target' : 'current',
            # open at the same page
            'type' : 'ir.actions.act_window',
        }


    # el def 2ele ta7t 3shan 2a7ot condition 3ala alert 2ele fe view, Note: when the month and day of (date_of_birth) == month and day of (today) rase the alert (122)
    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_test(self):  # this def come from appointment view <tree> that when group by patient apperd at the top of group clicke me button
        print("Clicked",f"patient name:- {self.name} and " ,f"his patient id:- {self.id}")
        # company = self.env["res.company"].browse(2)
        # # name = self.env["res.users"].browse(6).name
        # print(company.name)
        '''
        if not self.env["hospital.patient"].browse(5).mail: # rais error that 'hospital.patient' object has no attribute 'mail'
            print(self.env["hospital.patient"].browse(5).name,"..........................")
        '''

        return