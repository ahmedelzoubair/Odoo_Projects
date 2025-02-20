from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


# The below class means that the model will take the Functionality of the database tables but fields and data will not save  (create on the fly)
class CancelAppointment(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    # At the below method i will override the Functionality of the default method that responsible for add value to fields by default
    @api.model
    def default_get(self,fields): # => fields is the same concept of vals (dictionary well contains fields of the table) (78)
        res = super(CancelAppointment,self).default_get(fields) # => the main method return res (is a dictionary where the field names are keys and their corresponding default values are the values) so i will save the main data and i will add mine
        res['date_cancel'] = date.today() # => when calling model (cancel.appointment.wizard) by default field (date_cancel) will fill automatically with date.today() .
        if self.env.context.get('active_id'): # => checks if there is an active_id in the context. The (active_id) is typically the ID of the record that the user is currently interacting with. (if there is an ID from a related field)
            res['appointment_id'] = self.env.context.get('active_id') # => if the previous condition return true the appointment_id field = active_id, Note: (active_id) is reflect the (_rec_name) of the appointment model
        return res # => returns res dictionary with all data


    appointment_id = fields.Many2one('hospital.appointment', string="Appointment ID",
                                     domain=['|',('state','=','draft'),('priority','in',('1','2',False))])
    # Many2one relation is: models at odoo it`s a databases tables, So .Many2one relation means that i will take the primary key of (appointment) and put it as foreign key at (cancel_appointment)
    # domain => is attribute add a (condition) for appointment_id field (the appointment will appears at field)
    # ('state','=','draft') => (state) fields.Selection field at appointment model It`s contains the states of the appointment
    # ('priority','in',('1','2',False) => priority fields.Selection field at appointment It`s contains the (Number of stars) of the appointment
    # means: that the field will not appears only appointment that draft OR (|) contains 0,1 or 2 stars

    # Note: the value of appointment_id field will change as per as from where you open model


    reason = fields.Text(string="Reason")
    # fields.Text => same concept of char field but text extends according size of the words (63)
    date_cancel = fields.Date(string="Cancellation Date")

    # The below method will change the state of the appointment at special cases
    def action_cancel(self): #zorar cancel 2ele fe cancel appointment if date of appointment = todays date raise error
        cancel_days = self.env['ir.config_parameter'].get_param('Hospetal.cancel_days')
        # ir.config_parameter:- model save all conditions that created at settings (114)
        # get_param('Hospetal.cancel_days') :- get_param method will return a specific condition, Hospetal.cancel_days:- i create at model named (res_config_setting.py) that add Hospetal model to the setting and (cancel_days) is field conteans number of the dates
        allowed_days = date.today() - relativedelta.relativedelta(days=int(cancel_days))
        # relativedelta :- method that can calculate and get the differences between dates with all arguments of the date (month, day and year) in the same time, Note: we change (cancel_days) to int cuz it returns at string
        if self.appointment_id.appointment_date >= allowed_days:
            # note:- appointment_date and allowed_days must be same data type (fields.Date) cuz if DateTime bye bye kambora
            raise ValidationError(_(f"To cancel appointment must it is repeated on it {allowed_days} days "))
        else:
            self.appointment_id.state = 'cancel'


        # The below codes:- who Execute Queries by code when click cancel button (171 and 131)

        query = """select id,name from hospital_patient"""
        # the select line at SQL means (select all patients ids and names from hospital_patient model)
        self.env.cr.execute(query) # OR:- self._cr.execute(query)
        # cr :- cursor of environment, that will help to execute queries
        patients = self.env.cr.fetchall()
        # fetchall :- method that responsible to getting the result of query execution and save at variable
        print("all patients => ", patients) # => [(27, 'Sasa'), (5, 'Mohamed'), (11, 'Assem'), (4, 'Ahmed Sayed')]
        print("the id of the 1st selected patient => ",patients[0][0]) # => 27 (type int)
        # Note: if we change fetchall with dictfetchall => [{'id': 27, 'name': 'Sasa'}, {'id': 35, 'name': 'Mohamed'}], But:- at patients[0][0]) will get an error cuz it`s not the right way to get data from list contains dictionaries

        query2 = """select name from hospital_patient where id=4"""
        self.env.cr.execute(query2)
        patients2 = self.env.cr.fetchall()
        print("Patient who has ID number=4 => ",patients2) # => [('Ahmed Sayed',)]
        print("The name Directly => ",patients2[0][0]) # => Ahmed Sayed (type string)

        query3 = """select id,patient_id from hospital_appointment where id= %s""" % self.appointment_id.id    # Means That I will select (return) the appointment id and patient id (at hospital_appointment model) where (condition) the ID of the appointment is = the ID of selected appointment at appointment_id field of self (at cancel.appointment.wizard model)
        # id => appointment id
        # patient_id => at appointment model there is a relation between appointment and patient (Many2one relation), so patient_id related to the id of the patient that related with this current appointment
        # self.appointment_id.id => The appointment that will be selected at appointment_id field, What is appointment_id field:- is relation field (Many2one) with appointment model Note: at this case we don't care about the meaning of the relation but to his Functionality
        self.env.cr.execute(query3)
        patients3 = self.env.cr.fetchall()
        print(patients3)  # => [(22, 20)] :- 22 (appointment id) & 20 (patient id)
        # # TO add more than one "%s" (query3 = """select id,patient_id from hospital_appointment where id= %s and name= %s""" % (self.appointment_id.id, self.name))

        query4 = """
        SELECT 
            u.id AS user_id,
            u.login,
            g.id AS group_id,
            g.name AS group_name
        FROM 
            res_users u
        JOIN 
            res_groups_users_rel gu ON u.id = gu.uid
        JOIN 
            res_groups g ON gu.gid = g.id
        WHERE 
            u.login = 'ahmedsayed';
            """

        self.env.cr.execute(query4)
        patients4 = self.env.cr.fetchall()
        if patients4:
            print("User-Group Assignment Results:")
            for row in patients4:
                user_id, login, group_id, group_name = row
                print(f"User ID: {user_id}, Login: {login}, Group ID: {group_id}, Group Name: {group_name}")
        else:
            print("User 'ahmedelzoubair' is not assigned to any groups.")

        # The below return to make the page reloaded after press cancel button
        return {
            'type': 'ir.actions.client',
            # This tells Odoo that the action is client-side, meaning it will be handled by JavaScript running in the browser rather than by typical server-side logic.
            'tag': 'reload'

            # The below return make the wizard page not closing after press cancel button
            # return {
                    # 'type': 'ir.actions.act_window',
                    # 'view_mode': 'form',
                    # 'res_model': 'cancel.appointment.wizard',
                    # 'target': 'new',
                    # 'res_id': self.id
                    # # 'res_id': self.id :- to target open the same appointment form that I cancel
        }

    # the below method responsible for print PDF report
    def print_report(self):
        return self.env.ref('Hospetal.report_cancel_appointment_id_wizard').report_action()
        # data = {'form_data':self.read()[0]}
        # print("Data of self.read() =========>",self.read()[0]) # => Data of self.read() =========> [{'id': 55, 'appointment_id': (2, 'AP00004'), 'reason': 'txt from cancel button of the form view', 'date_cancel': datetime.date(2024, 11, 27), '__last_update': datetime.datetime(2024, 11, 27, 10, 53, 20, 751169), 'display_name': 'cancel.appointment.wizard,55', 'create_uid': (2, 'Mitchell Admin'), 'create_date': datetime.datetime(2024, 11, 27, 10, 53, 20, 751169), 'write_uid': (2, 'Mitchell Admin'), 'write_date': datetime.datetime(2024, 11, 27, 10, 53, 20, 751169)}]
        # # appointments = self.env['hospital.appointment'].search_read([])
        # # Note: (search_read) method at env to get Lots of data [all relations between 2 models] as dictionary but (search_count) method at env to search for numbers of related inherit objects from anther model ,
        # print("Data of search_read([]) =========>", self.env['hospital.appointment'].search_read([]))
        #
        # domain = []
        # get_appointment_id_selected = self.read()[0].get('appointment_id')[0]
        # if get_appointment_id_selected:
        #     domain += [('appoint_id','=',get_appointment_id_selected)]
        #
        # print("Data of domain =========>", domain)
        # appointments = self.env['hospital.appointment'].search_read(domain)
        #
        # data = {
        #     'form_data' : self.read()[0],
        #     'appointments' : appointments
        # }
        # return self.env.ref('Hospetal.report_cancel_appointment_wizard').report_action(self,data=data)
        # # self.env.ref => This fetches the report's record using its XML ID: Hospetal.report_cancel_appointment_wizard. Ensure this ID is correct and matches your report's configuration.
        # # report_action(self) => This method generates the report as a PDF and allows it to be downloaded or opened in the browser.
        # # data=data => the (1st data) is parameter related to (report_action) method saving data inform of dictionary and (2nd data) is a Python dictionary created in this method. It contains a key-value named (form_data) and his value is (a dictionary representing the current record's fields and values).
        # # Note: self.read() get data or not according to [def default_get(self,fields):] method bring data or not
