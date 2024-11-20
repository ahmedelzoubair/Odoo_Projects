# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    confirmed_user_id = fields.Many2one('res.users',string="Confirmed User",store=True)
    # to check that add to Db:- Technical => Models => search (sale.order) => search (sale.confirmed_user_id) @<notebook> => <page name="Miscellaneous"> => In Apps: om_odoo_inheriteence=> ya3ni el field dah gay men 2anhi model

    # I will call action_confirm method (that related to click the confirm button at Sales Order )
    def action_confirm(self):
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id
        # means that the new field will take the user id of the confirmed user


    # To Pass New Field (confirmed_user_id) Value From Sale Order To Invoice In Odoo:- we need 1st to update the below method
    def _prepare_invoice(self):
        # This method is responsible for preparing the values (a dictionary of field-value pairs) that will be used to create an invoice (account.move) when an invoice is generated from a sale order (sale.order).

        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        # By calling [ super(SaleOrder, self)._prepare_invoice() ],  we’re executing the original _prepare_invoice method, which prepares the standard invoice data based on the sale order’s fields.
        # invoice_vals :- is the result of this call is a dictionary of values (invoice_vals) that Odoo uses to create an account.move record (the invoice).
        # Note:- when search with (_prepare_invoice) method (at: sale/models/sale_order.py), search with (invoice_vals) you will se that (invoice_vals) is dictionary contains default values such as partner_id, currency_id, and other necessary fields from the sale order to the invoice.

        # Set sale_order_id in account.move to link back to this sale order
        invoice_vals['sale_order_id'] = self.id
        """""
        invoice_vals['sale_order_id'] :- i will add a new key (sale_order_id) and new value (self.id) to the dic (invoice_vals) to add them to the gather information from the sale order to populate the invoice fields
        Note:- account.move doesn’t have a (sale_order_id) field by default. We added sale_order_id in account.move to store a reference to the related sale order. This sale_order_id is a Many2one relationship to sale.order, meaning it will store a link to a specific sale order record.
        """""


        return invoice_vals
        # return the final invoice_vals dictionary


