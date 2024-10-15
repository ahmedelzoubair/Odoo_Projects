from odoo import api, fields, models, _


# ana hena 3aml tabel 2asagl feh el patient
class PatientsTags(models.Model):
    _name = "patients.tags"
    _description = "Patients Tags"

    name = fields.Char(string="Tag", required=True)
    active = fields.Boolean(string="Active", default=True)
    color_of_tag = fields.Integer(string="Color", copy=False) # copy=False :- 3shan lama 2a3ml duplicate color don't copy
    sequence = fields.Integer(string="Sequence")

    # el method 2ele ta7t 3shan 2azawed option 3ala button Duplicate
    @api.returns('self',lambda value: value.id)     #=> 3shan 2awsl le func 3l (copy) lazm 2aro7 le dictionary (api) gowa (returns) (84) NOTE: el hendi mashar7sh el prameters
    def copy(self, default=None):                         #=> da5alna gowa methoud copy we lazm prameters de, (default) like vals we fileds
        if default is None:                               #=> lo default rg3 Empty rag3 el dict Empty
            default = {}

        if not default.get('name'):                     #=> lo default rg3 feh (name)
            # default['name'] = self.name + " (Copy)"   #=> rag3 el name + Copy
            default['name'] = _("%s (Copy)", self.name)

        default['sequence'] = self.sequence + 1         #=> 3shan 2nd sql (check_sequence) reg3 0 or less
        return super(PatientsTags,self).copy(default)

    _sql_constraints = [('unique_tag_name','unique (name,active)','Name Must Be Unique'),
                        ('check_sequence','check (sequence > 0)','sequence Must Be > 0')]
    # el sql_constraints 3shan add conditions to filed, (unique_tag_name) constraints name [ana 2ele me5taro 3ala mazagi],
    # (unique) constraints type, we constraints dah 3shan yt7a22 lazm yekon el tow fileds = true (name) metkarr we not archived
    # (name) filed name, we 3amlt add lel active 3shan el condition yet7a22 lama 2l name ytkarr we
    # 'mass if repetition the name' (82)
    # Note: sql constraints has no effect at compute fileds

