from email.policy import default
from re import search

from dateutil.utils import today

from odoo import api, fields, models, _, SUPERUSER_ID
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta

from odoo.tools.populate import compute


# The below class related to patient table
class HospitalPatients(models.Model):
    # (models.Model) => When you define a model by inheriting from models.Model, you are creating a persistent database model in Odoo.
    # models => is a module (or package) provided by Odoo,
    # Model => is a class inside the models module.

    _name = "hospital.patient"
    _description = "Hospital Patient"
    _inherit = ['mail.thread', 'mail.activity.mixin'] # we inherit the functions of (mail.thread) and (mail.activity.mixin) to can create shutter
    # 'mail.thread' :- responsible to bring the tracking fields
    # _rec_name = 'name'

    name = fields.Char(string="Name", tracking=True, required=True)
    # The fields you define in the model map to columns in the database table.
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')])
    date_of_birth = fields.Date(string="Patient Birth Day")
    age = fields.Integer(compute='_compute_age', inverse="_inverse_compute_age", store=True,tracking=True)  # note:- the compute filed do not store by default in database
    # inverse:- parameter in an Odoo field declaration is used to define the method that computes the inverse operation of a computed field (99)
    # search='_search_age':- parameter in a field definition is used to define a custom search method for the field, and add this parameter to the compute field (100)
    # store=True:- compute filed will save at Database
    active = fields.Boolean(string="Active", default=True)
    ref = fields.Char(string="Reference", readonly=True)
    image = fields.Image(string="Image")
    appointment_count = fields.Integer(string="Appointment Numbers", compute='_compute_appointment_count',store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    # fields.One2many => It creates a parent-to-child relationship between models. (that means: as per SQL consent that the primary key of the parent table (.patient) will save as foreign key at the child table (.appointment)
    tags_ids = fields.Many2many('patients.tags', string="Tags")
    # it`s a relationship with (patients.tags) module to create tags, as per SQL consent that the primary key of (hospital.patient) model and primary key of (patients.tags) model will save as foreign keys at 3rd table
    parent = fields.Char(string="Parent Name")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status",trace=True)
    partner_name = fields.Char(string="Partner Name")
    is_birthday = fields.Boolean(string="Is Birthday", compute='_compute_is_birthday')
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")

    # this method that responsible for create function at odoo, take parameters (self,vals)
    @api.model
    # api => a module provided by Odoo. It contains various (alot of diff) decorators and helpers to define and manage model methods.
    # model => a property of the api module. So when you use @api.model, you’re calling a decorator provided by api to define model-level methods.
    def create(self,vals):  # => this method that responsible for create function at odoo, take parameters (self,vals), (self) related to object will created form class, (vals) vals:- is the dictionary that contains the initial values that are used to create the new record, holding the field data that will be stored in the database. Example (vals = {'name': 'John Doe', 'age': 30})
        # super(HospitalPatients, self).create(vals) => (super) that means I will "override" the main class with the below function
        # vals['ref']= "OMTEST" => get the 'ref' attribute add in it value (OMTEST)
        vals['ref'] = self.env['ir.sequence'].next_by_code('patient.sequence')  # => self.env['ir.sequence']:- call env od model ir.sequence ('ir.sequence'):- model that content all sequ ways of the sys, (next_by_code):- method that related to add sequ as per rule,(patient.sequence):- code (that call sequ) related to sequ patient (72) Hospetal => data => sequence_data_patient.xml
        return super(HospitalPatients, self).create(vals)  # return main create function and add to her functionality (make ref=OMTEST)
        # Note: if I call super first will implement all Functionality of the create method the implement my "override" code and vice versa

    # this methode that responsible for Edite function at odoo, take parameters (self,vals)
    def write(self,vals):
        # vals => dictionary related to all fields at model
        if not self.ref and not vals.get('ref'):  # => if ref (field) at self (hospital.patient) not none (has value) {and} at dictionary vals there is no value at key ref
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

    # The below method is closely related to the Odoo environment. It is a special method in Odoo used to define how records of a model are displayed as strings in the user interface, such as in dropdowns, Many2one fields, and other relational contexts.
    def name_get(self):
        # result = []
        # for record in self:
        #     name = record.ref + "/" + record.name
        #     result.append((record.id, name))
        # return result
        return [(record.id, "[%s] %s" % (record.ref, record.name)) for record in self]  # (75)

    # The below method related to delete button
    @api.ondelete(at_uninstall=False)  # (at_uninstall=False):- That means if Hospetal model uninstall the below def will not run, (=True) the method would be executed even during the uninstallation of the module
    def _check_appointment(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("Can not delete this patient because has appointment "))


    @api.constrains('date_of_birth')  # api.constrains => For validation,Raises errors if constraints are violated,Prevents records from being saved if validation fails.
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth >= fields.Date.today():  # => if patient birth date > or = date of today (date_of_birth = 0 or -1) raise ValidationError
                raise ValidationError(_("The Date That You Add Is Not Acceptable"))

    @api.depends('date_of_birth')  # api.depends => For computed fields that depend on other fields.(when change at filed execute the below code
    def _compute_age(self):  # => self each object that will generate from the class (patient). (hassan, omar, gamal,....)
        for rec in self:  # => Loops through each attribute in the patient record. Each rec depends to (name, age,...). This ensures that when I need to get name of any patient => rec.name
            today = date.today()  # date => class related to datetime model , today() => method that responsible for get the date of today
            if rec.date_of_birth:  # => if date_of_birth field has value (not = none) Execute the below code
                rec.age = today.year - rec.date_of_birth.year  # Subtract the year that goes back to today's date (2025) from year that goes back to date_of_birth filed then enter the result in age field that related to the selected patient (self)
            else:
                rec.age = 0 # => if date_of_birth field = none , add 0 to age field (I put that condition to avoid errors that will come from patients that has no date_of_birth add yet)

    @api.onchange('age')  # when change at age filed execute the below code (99)
    def _inverse_compute_age(self):
        today = date.today()
        for rec in self:
            rec.date_of_birth = today - relativedelta.relativedelta(years=rec.age)
            # relativedelta is part of the "relativedelta" library and is used to perform relative date calculations. It allows you to add or subtract specific time periods, such as years, months, days, etc.
            # years=rec.age means that the relative delta is calculated based on the age of the record (rec.age), which is assumed to be an integer representing the person's age in years.
            # For example, if today's date is 2024-09-02 and (years of rec.age = 25), it calculates the date_of_birth by subtracting 25 years from today's date.

    def _search_age(self, operator,value):  # this how to create search fun must add operator and value (value:- the int number add by user then search with it by age) parameter (100)
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)  # field (date_of_birth) = (today date - tare5 el value add by cust) for ex:- if value today = 10/9/2024 , value = 24 ( relativedelta.relativedelta(years=value) = 24 ) then date_of_birth = 10/9/2020
        # return [('date_of_birth','=',date_of_birth)] # el return de hatgeb koll mawaled 2020 {bass} just [10/9] not all in 2020 so this return not work
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]
        # date_of_birth date filed means it`s same date.today() continue day, month and year
        # start_of_year:- date_of_birth (2020) replace at day (1) month (1)
        # end_of_year:- date_of_birth (2020) replace at day (31) month (12)
        # then this return will get all of people of all the year no like the previous comment return
    # Note: I remove this function from code because when search with character (letter) and select age rase an python error so make date_of_birth field store=True to prevent this error. Why does this error appear? cuz at xml view I add a condition (filter_domain="['|', ('name', 'ilike', self), ('age', 'ilike', self)]")


    @api.depends('appointment_ids')  # =>  appointment_ids:- it`s filed one2many with appointment model means one patient can have alot of appointments, That means when depends on that field well calculate (get) all ids of appointments that related with ids of patients
    def _compute_appointment_count(self):
        # appointment_group = self.env['hospital.appointment'].read_group(domain=[],fields=[],groupby=[]) => read_group : method in Odoo's ORM. This method is used to perform grouping and aggregation of records, similar to SQL's GROUP BY and aggregate functions like COUNT, SUM  (128)
        appointment_group = self.env['hospital.appointment'].read_group(domain=[], fields=['patient_id'], groupby=['patient_id'])  # (128) domain=[('state','=','done')] => will get only done app
        # calling method (read.group) [fields: Specifies the fields to include in the result. In this example, 'patient_id' is a Many2one field in the hospital.appointment model that refers to the hospital.patient model.] [groupby: Specifies the field(s) to group by. In your case, grouping is based on the patient_id field. This means all appointments related to the same patient (patient_id) will be grouped together.]
        for app in appointment_group:  # el for de 3shan 2a3adi 3ala koll filed (same of for loop at self)
            # if we print app => {'patient_id_count':9, 'patient_id':(3, <odoo.tools.func.lazy obj>), '__domain':[('patient_id','=',3)]} # patient_id_count:- filed Generated auto from (.read_group) to count elements (num) that related between hospital.patient and hospital.appointment
            patient_id = app.get('patient_id')[0]  # [0]:- to get 1st element at tuble (id) => 3
            patient_rec = self.browse(patient_id)  # .browse() :- is a method provided by Odoo's ORM (Object-Relational Mapping) that is used to create recordsets. It retrieves records from the database by their IDs and allows you to interact with them as Python objects., patient_id:- the id that comining from (.read_group)
            patient_rec.appointment_count = app.get('patient_id_count')  # after getting all fields of patient with id (3) i will target appointment_count add put in it patient_id_count (9) that created from read_group methode
            self = self - patient_rec # Subtract patients (self) that contains calculated (appointment_count) from all patients (self)
            # 27na fe loop betgeb koll el relation elements between two models, so => main self [hospital.patient(2,3,14,17,50)] = self [hospital.patient(2,3,14,17,50)] - patient_rec [hospital.patient(2,)] de 2awll mara
            # then fe tane mara ba2t el (main self) = [hospital.patient(3,14,17,50)]
            # then el (patient_rec) hatgeb koll relation elements [ma3ada] el elements 2ele mafesh mabenhom relation [hospital.patient(17) and hospital.patient(50)]
            # then final self = hospital.patient(17,50)
        self.appointment_count = 0
        # after looping for all patients Number of patients to minus that have not any appointments the appointment_count field (hospital.patient(17,50)) = 0

        # ---------------------------------------------------------------------
        # for rec in self:
        #     rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
        # => self.env['hospital.appointment'] :- calling the env of appointment model
        # => search_count :- method at env to search for numbers of related inherit objects from anther model  ..
        # => [('patient_id','=',rec.id)] :- is the condition of method (filed el relation between two models),
        # patient_id:- dah filed many2one gowa appointment rabt el appointment with patient
        # rec.id:- this is the unique filed created by system by default
        # Note: (search_count) get the previous, (search_read) get Lots of data as dictionary

    # The below def related to operation of smart button:- smart button will open the appointments that related to the patient
    def action_view_appointments(self):
        return{
            'name' : _('Appointments'),
            'res_model' : 'hospital.appointment',
            'view_mode' : 'list,form',
            'context' : {'default_patient_id':self.id},
            # Passing default patient_id via context, The context s a dictionary that provides additional information influencing how data is processed and displayed. In this case, it ensures that when the user creates a new appointment, the patient_id field is already filled in with the current patient’s ID.
            'domain' : [('patient_id','=',self.id)],
            # Add a condition to the view to open the appointments that related to the patient id of self
            'target' : 'current',
            # open at the same page
            'type' : 'ir.actions.act_window',
        }


    # The below method for make is_birthday field (bool) as per the below condition (122)
    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    # when the month and day of (date_of_birth) == month and day of (today) rase the alert
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_test(self):  # this def come from appointment view <tree> that when group by patient apperd at the top of group clicke me button
        print("Button Clicked..",f" Patient name:- ({self.name}) & ", f" Patient id:- ({self.id})")
        # company = self.env["res.company"].browse(2)
        # # name = self.env["res.users"].browse(6).name
        # print(company.name)
        elzoubair_user = self.env.ref('Hospetal.ahmed_elzoubair_user')
        elzoubair_id = elzoubair_user.id
        print(f"The ID of user Ahmed EL Zoubair = {elzoubair_id}")
        elzoubair_name = self.env["res.users"].browse(elzoubair_id).name
        print(f"The Name of user ID (8) is = {elzoubair_name}")
        print(f"The type of elzoubair_user is. {type(elzoubair_id)}, And type of elzoubair_name is. {type(elzoubair_name)}")
        return
