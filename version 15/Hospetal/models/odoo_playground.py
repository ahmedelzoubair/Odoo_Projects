from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval


# ana hena 3aml tabel 2asagl feh el patient
class OdooPlayground(models.Model):
    _name = "odoo.playground"
    _description = "Odoo Playground"

    DEFAULT_ENV_VARIABLES = """# Available variables for env (after 77)
        - self => self is related to the obj that created from the class (odoo.playground). 
        Execute= odoo.playground(1,) => (1) is the ID
        - self.env => env de class gowa odoo => api, el class de feha a lot func
        Execute= <odoo.api.Environment object at 0x7fca118b3a30> 
        - self.env.user  => func (user) related to the record set of current logged in user (Mitchell Admin)
        Execute= res.users(2,) => (res.users) model (database) feha all users, (2) user id (elf.env.user.name=Mitchell Admin)
        - self.env.company => bygblk el company 2ele 2nta feha (fe 7en en el sherka leha 2akr men company) (self.env.company.name = My Company (San Francisco))
        Execute= res.company(1,)
        - self.env.companies => return whether companies of users
        Execute= res.company(1,3)
        - self.env.lang
        Execute= en_US
        - self.env.context => context is actually a single dictionary that can be shared across different parts of the system, including Python code, XML views, and action menus. It acts as a global dictionary that byfhm kol
        Execute= {'lang': 'en_US', 'tz': 'Africa/Cairo', 'uid': 2, 'allowed_company_ids': [1], 'params': {'cids': 1, 'menu_id': 378, 'action': 570, 'model': 'odoo.playground', 'view_type': 'form', 'id': 1}}
        tz (time zone), uid (user id), 
        - self.env.context.get('tz') => el (context) dictionary 3shan 2ageb meno 2ee data 2sta3ml methoed (get) we tz de y3ni tezak :D la2 y3ni time zone xD
        Execute= Africa/Cairo
        - self.env["hospital.appointment"].browse(3).patient_id.name => (.env["hospital.appointment"]) ro7 le (hospital.appointment) / ( .browse(3) ) 3 obj created (id) / (.patient_id) related field with patien / (.name) 2smo
        Execute= sayed
        - self.env["hospital.appointment"].browse(3).action_done() 
        Execute= el appointment id(3) el state hatb2a done 3shan el (action_done()) method gowa 
        - self.env.ref('Hospetal.housewife_tag').name => (housewife_tag) dah id le patient tage mawgod gowa data => patient_tags_data.xml
        Execute= Housewife => note: debug => View Metadata lo leh (XML ID) yagoz 3aleh el (self.env.ref)
        - self.env.ref('__export__.hospital_patient_2_22fe4b69').name => lama raf3t el data be XML sheet 5ad id Metadata ('__export__.hospital_patient_2_22fe4b69') we 3rft 2ageb meno (name)
        Execute= ahmed 
        - name = self.env["res.users"].browse(6).name => res.users:- model 2ele feh users , (browse) method ba7ot feha id (6) yegebli koll 7aga 3an 2ele id = 6
        Execute= Marc Demo 
        company = self.env["res.company"].sudo().browse(2) (then) company_name = company.name (then) use company_name to get the n name of company 
        Execute= EG Company
    """

    model_id = fields.Many2one('ir.model',string="Model")
    code = fields.Text(string="Code")
    result = fields.Text(string="Result")

    def action_execute(self):
        try:
            if self.model_id:
                model = self.env[self.model_id.model]
            else:
                model = self
            self.result = safe_eval(self.code.strip(), {'self': model})
        except Exception as e:
            self.result = str(e)