# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2020-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_pos = fields.Many2many('pos.config', string='Allowed Pos',help='Allowed Pos for this user')
    # allowed_pos: This is a Many2many field that links a user to multiple POS configurations
    show_users = fields.Boolean(string="Show users of pos", default=True, help='Show users in dashboard ( for pos administrators only)')
    # show_users: This is a Boolean field that determines whether the users of a POS should be displayed in the dashboard.

    @api.model
    def create(self, vals):
        self.clear_caches()
        return super(ResUsers, self).create(vals)

    def write(self, vals):
        # for clearing out existing values and update with new values
        self.clear_caches()
        return super(ResUsers, self).write(vals)


class PosConfig(models.Model):
    _inherit = 'pos.config'

    users_allowed = fields.Many2many('res.users', compute='get_allowed_users')
    # users_allowed: This is a computed Many2many field that dynamically determines which users are allowed to access a specific POS configuration.

    # This method computes the value of the users_allowed field.
    def get_allowed_users(self):
        for this in self:
            if this.env.user.show_users:
            # checks if user who is open POS model (this.env.user) has the show_users field set to True (Note: show_users field is default=True)
                this.users_allowed = self.env['res.users'].search([('allowed_pos', '=', this.id)])
                # this.users_allowed => (users_allowed) field at (pos.config)
                # self.env['res.users'] => refers to the res.users model, which represents the users in the Odoo system.
                # .search => The argument passed to (search) is a domain, which is a list of conditions used to filter records.
                # allowed_pos => This is the Many2many field in the res.users model that links users to pos.config model
                # this.id => This refers to the id of the current pos.config record (i.e., the current POS configuration
            # The domain means: retrieves all users who are allowed to access the current POS configuration

            # as per there is a  Many2many relation between (res.user) and (pos.config) will create 3rd table at the database Contains the primary keys (id) of the two tables (res.user) and (pos.config),
            # That means all user can access all POS configurations and vice versa.
            # ..But in this case i will make a many2many relation with condition.
            # They are inverse relationships: If User A has allowed_pos = [1, 2], then: POS configuration 1 will include User A in its users_allowed. POS configuration 2 will also include User A in its users_allowed.


            else:
                this.users_allowed = None


