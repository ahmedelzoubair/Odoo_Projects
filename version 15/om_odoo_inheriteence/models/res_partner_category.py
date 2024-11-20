# -*- coding: utf-8 -*-

from odoo import models, fields, api


# At the below we will add oe_chatter to (Contacts model => Configuration => Contact Tags => Employees)
class ResPartnerCategory(models.Model):
    _name = 'res.partner.category'
    # Note:- At this case without add name will facing => ValueError: The _name attribute ResPartnerCategory is not valid. cuz we add 2 models at _inherit
    _inherit = ['res.partner.category', 'mail.thread'] # Note:- don`t forget to add (mail model) at the manifest depends
    # res.partner.category:- Table that Contains (Contact Tags) imagine xD

    name = fields.Char(tracking=True)
    # Note:- to add attribute like tracking maybe at fields.Char not need to tale all field from original model, just add new attribute




