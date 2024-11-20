from odoo import api, fields, models, _


# ana hena 3aml tabel 2asagl feh el patient
class PatientsTags(models.Model):
    _name = "patients.tags"
    _description = "Patients Tags"

    name = fields.Char(string="Tag", required=True)
    active = fields.Boolean(string="Active", default=True)
    color_of_tag = fields.Integer(string="Color", copy=False) # copy=False :- 3shan lama 2a3ml duplicate color don't copy
    sequence = fields.Integer(string="Sequence")
    hint = fields.Char(string="Hint", trim=False)
    # trim=False => to make field save spaces

    # el method 2ele ta7t 3shan 2azawed option 3ala button Duplicate (84)
    @api.returns('self',lambda value: value.id)
    # This is a decorator in Odoo's API system. It specifies that the method will return a two records ('self') and (vals) it instructs {ya2mor} the method to return the ID of the copied record and put it in vals
    def copy(self, default=None):  #=> (default) dictionary re specify and is used to specify default values that will be used in the duplicated record.
        if default is None:
            default = {}
        # If no default dictionary is passed when the copy method is called, this ensures that default is an empty dictionary so that you can add custom default values to it.
        # if the code didn't include the if default is None: default = {} check, and you later try to use default as a dictionary, you'd get an error. You can't treat None as a dictionary (i.e., None.get() would raise an error).
        if not default.get('name'):
            # default.get('name') returns None cuz I make (default=None) so default.get('name') return none (false)
            # so, not default.get('name') return true
            default['name'] = _("%s (Copy)", self.name) # => then make the name at default = self.name + " (Copy)"
            # default['name'] = self.name + " (Copy)"   #=> rag3 el name + Copy

        default['sequence'] = self.sequence + 1         #=> 3shan 2nd sql (check_sequence) reg3 0 or less
        # default = default or {}  # Initialize default as an empty dictionary if it's None
        # default['name'] = default.get('name',"%s (Copy)" % self.name)  # Set 'name' directly, with fallback to "Original Name (Copy)"
        # default['sequence'] = self.sequence + 1
        # return super(PatientsTags, self).copy(default)
        return super(PatientsTags,self).copy(default)

    _sql_constraints = [('unique_tag_name','unique (name,active)','Name Must Be Unique'),
                        ('check_sequence','check (sequence > 0)','Sequence Must Be > 0')]

    # el sql_constraints 3shan add conditions to filed, (unique_tag_name) constraints name [ana 2ele me5taro 3ala mazagi],
    # (unique) constraints type, we constraints dah 3shan yt7a22 lazm yekon el tow fileds = true (name) metkarr we not archived
    # (name) filed name, we 3amlt add lel active 3shan el condition yet7a22 lama 2l name ytkarr we
    # 'mass if repetition the name' (82)
    # Note: sql constraints has no effect at compute fileds

