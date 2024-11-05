# -*- coding: utf-8 -*-

from odoo import models, fields, api

# el inherit 2ele ta7t 3shan 2msa7 option men el access right 2ele mawgoda fe users ta7t Technical list (117)
class ResGroups(models.Model):
    _inherit = 'res.groups' # res.groups:- dah el model 2ele feh koll access rights 2ele ta7t Technical list


    def get_application_groups(self, domain): # this is the function that responsible to return the user groups
        group_id = self.env.ref('stock.group_reception_report').id
        # ref('').id :- hatli el id lel reference 2ele gowa ()
        # stock.group_reception_report:- dah el XML lel access right that named (Use Reception Report), settings => => users&companies => groups => search by name => depuger => metadata
        return super(ResGroups,self).get_application_groups(domain + [('id','!=',group_id)])
        # return super(ResGroups,self).get_application_groups(domain + [('id','not in',(group_id,2nd_group_id))])




