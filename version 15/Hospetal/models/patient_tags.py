from odoo import api, fields, models, _


class PatientsTags(models.Model):
    _name = "patients.tags"
    _description = "Patients Tags"

    name = fields.Char(string="Tag", required=True)
    active = fields.Boolean(string="Active", default=True)
    color_of_tag = fields.Integer(string="Color", copy=False) # copy=False :- to when I duplicate tage color don't copy
    sequence = fields.Integer(string="Sequence")
    hint = fields.Char(string="Hint", trim=False)
    # trim=False => to make field save spaces

    # The below method add more option at Duplicate button (84)
    @api.returns('self',lambda value: value.id)
    # This is a decorator in Odoo's API system. It specifies that the method will return two records ('self') and (value) it instructs {yegber} the method to return the ID of the copied record and put it in value
    def copy(self, default=None):  #=> (default) dictionary and is used to specify default values that will be used in the duplicated record.
        if default is None:
            default = {}
        # If no default dictionary is passed when the copy method, this ensures that default is an empty dictionary so that you can add custom default values to it.
        # if the code didn't include the if default is None: default = {} check, and you later try to use default as a dictionary, you'd get an error. You can't treat None as a dictionary (i.e., None.get() would raise an error).
        if not default.get('name'):
            # default.get('name') returns None cuz I make (default=None) so default.get('name') return none (false)
            # so, not default.get('name') return true
            default['name'] = _("%s (Copy)", self.name) # => then make the name at default = self.name + " (Copy)"
            # default['name'] = self.name + " (Copy)"   #=> return name + Copy

        default['sequence'] = self.sequence + 1         #=> cuz 2nd sql (check_sequence) return 0 or less rase error
        # default = default or {}  # Initialize default as an empty dictionary if it's None
        # default['name'] = default.get('name',"%s (Copy)" % self.name)  # Set 'name' directly, with fallback to "Original Name (Copy)"
        # default['sequence'] = self.sequence + 1
        # return super(PatientsTags, self).copy(default)
        return super(PatientsTags,self).copy(default)

    _sql_constraints = [('unique_tag_name','unique (name,active)','Name Must Be Unique'),
                        ('check_sequence','check (sequence > 0)','Sequence Must Be > 0')]

    # el sql_constraints to add conditions to the filed, (unique_tag_name) constraints name of the condition
    # (unique) constraints type, and this constraintsTo be achieved name must be unique if tage active or not (82)
    # Note: sql constraints has no effect at compute fields

