from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    # Many2many field to select multiple customers
    partner_ids = fields.Many2many(
        'res.partner',
        'payment_term_customer_rel',  # relation table name
        'payment_term_id',  # column for payment term
        'customer_id',  # column for customer
        string='Customers',
        help="Select customers that can use this payment term"
    )


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('partner_id')
    def _compute_invoice_payment_term_id(self):
        super(AccountMove, self)._compute_invoice_payment_term_id()
        for move in self:
            try:
                if move.is_sale_document(include_receipts=True) and move.partner_id:
                    applicable_terms = self.env['account.payment.term'].search([
                        ('partner_ids', 'in', move.partner_id.id)
                    ], limit=1)
                    if applicable_terms:
                        move.invoice_payment_term_id = applicable_terms
                        _logger.debug("Selected payment term for partner %s: %s",
                                     move.partner_id.name, applicable_terms.name)
                    else:
                        move.invoice_payment_term_id = move.partner_id.property_payment_term_id or False
                        _logger.debug("No applicable terms found for partner %s, using default: %s",
                                     move.partner_id.name, move.invoice_payment_term_id.name if move.invoice_payment_term_id else 'None')
                else:
                    move.invoice_payment_term_id = move.partner_id.property_payment_term_id or False
            except Exception as e:
                _logger.error("Error computing invoice_payment_term_id for move %s: %s", move.name, str(e))
                move.invoice_payment_term_id = move.partner_id.property_payment_term_id or False


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('partner_id')
    def _compute_payment_term_id(self):
        super(SaleOrder, self)._compute_payment_term_id()
        for order in self:
            try:
                if order.partner_id:
                    # Purpose: Checks if the sales order has a customer selected (partner_id is not empty).
                    applicable_terms = self.env['account.payment.term'].search([('partner_ids', 'in', order.partner_id.id)], limit=1)
                    # accesses the (account.payment.term) model from the environment
                    # The domain [('partner_ids', 'in', order.partner_id.id)] filters payment terms where the partner_ids field (a Many2many field) includes the ID of the selected customer (order.partner_id.id).
                    # self.env['account.payment.term'].search([('partner_ids', 'in', order.partner_id.id)] => go to model => get
                    # limit=1 ensures only one payment term is returned (the first match, based on the default order, typically ID or name). This avoids ambiguity if multiple payment terms are linked to the customer.
                    if applicable_terms:
                        # if applicable_terms not = none
                        order.payment_term_id = applicable_terms
                        # go to payment_term_id field of sale.order make it = applicable_terms
                        _logger.debug("Selected payment term for partner %s in sale order %s: %s",
                                     order.partner_id.name, order.name, applicable_terms.name)
                    else:
                        order.payment_term_id = order.partner_id.property_payment_term_id or False
                        # order.partner_id.property_payment_term_id :is the default payment term configured for the customer in the res.partner model (a Many2one field to account.payment.term).
                        # or False :means None
                        _logger.debug("No applicable terms found for partner %s in sale order %s, using default: %s",
                                     order.partner_id.name, order.name, order.payment_term_id.name if order.payment_term_id else 'None')
                else:
                    order.payment_term_id = False
                    # if order.partner_id = None (no cust at partner_id) make payment_term_id = False
            except Exception as e:
                _logger.error("Error computing payment_term_id for sale order %s: %s", order.name, str(e))
                order.payment_term_id = order.partner_id.property_payment_term_id or False
