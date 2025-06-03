from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def create(self, vals):
        order = super().create(vals)
        order._propagate_analytic_distribution()
        return order

    def write(self, vals):
        res = super().write(vals)
        self._propagate_analytic_distribution()
        return res

    def _propagate_analytic_distribution(self):
        for order in self:
            lines = order.order_line
            if not lines:
                continue
            first_line = lines[0]
            dist = first_line.analytic_distribution
            for line in lines:
                if line != first_line:
                    line.analytic_distribution = dist.copy()
