from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']

    analytic_distribution = fields.Json(
        string="Analytic Distribution"
    )

    analytic_precision = fields.Integer(
        string="Analytic Precision",
        default=lambda self: self.env['decimal.precision'].precision_get('Analytic')
    )

    @api.onchange('analytic_distribution')
    def _onchange_analytic_distribution(self):
        """Update analytic_distribution on all order lines when changed on PO"""
        if self.analytic_distribution:
            for line in self.order_line:
                line.analytic_distribution = self.analytic_distribution

    def write(self, vals):
        """Update lines when analytic_distribution is modified via write"""
        res = super(PurchaseOrder, self).write(vals)
        if 'analytic_distribution' in vals:
            for order in self:
                order.order_line.write({
                    'analytic_distribution': vals['analytic_distribution']
                })
        return res


class PurchaseRequisition(models.Model):
    _inherit = ['purchase.requisition']

    analytic_distribution = fields.Json(
        string="Analytic Distribution"
    )

    analytic_precision = fields.Integer(
        string="Analytic Precision",
        default=lambda self: self.env['decimal.precision'].precision_get('Analytic')
    )

    @api.onchange('analytic_distribution')
    def _onchange_analytic_distribution(self):
        """Update analytic_distribution on all order lines when changed on PO"""
        if self.analytic_distribution:
            for line in self.line_ids:
                line.analytic_distribution = self.analytic_distribution

    def write(self, vals):
        """Update lines when analytic_distribution is modified via write"""
        res = super(PurchaseRequisition, self).write(vals)
        if 'analytic_distribution' in vals:
            for order in self:
                order.line_ids.write({
                    'analytic_distribution': vals['analytic_distribution']
                })

        return res

    def action_in_progress(self):
        """Override to set analytic_distribution when creating new RFQs"""
        res = super(PurchaseRequisition, self).action_in_progress()

        if self.analytic_distribution:
            # Update all related draft purchase orders
            for purchase in self.purchase_ids.filtered(lambda p: p.state == 'draft'):
                purchase.write({'analytic_distribution': self.analytic_distribution})
                purchase.order_line.write({
                    'analytic_distribution': self.analytic_distribution
                })

        return res


