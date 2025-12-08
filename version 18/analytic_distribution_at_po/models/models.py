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

