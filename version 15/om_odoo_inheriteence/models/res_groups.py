# -*- coding: utf-8 -*-

from odoo import models, fields, api

# el inherit 2ele ta7t 3shan 2msa7 option men el access right 2ele mawgoda fe users ta7t Technical list (117)
class ResGroups(models.Model):
    _inherit = 'res.groups' # res.groups:- dah el model 2ele feh koll access rights 2ele ta7t Technical list


    def get_application_groups(self, domain):
        # this is the function that responsible to return the user groups
        group_id = self.env.ref('stock.group_reception_report').id
        # ref('').id :- get the id to the reference between ()
        # stock.group_reception_report:- (stock) is the folder that contain all access rights of the system, (group_reception_report) is the XML ID that related to (Use Reception Report)
        # To get XML ID of specific access right, settings => => users&companies => groups => search by name => depuger => metadata
        return super(ResGroups,self).get_application_groups(domain + [('id','!=',group_id)])
        # return super(ResGroups,self).get_application_groups(domain + [('id','not in',(group_id,2nd_group_id))])




