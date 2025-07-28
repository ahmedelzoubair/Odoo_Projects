from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    warehouse_id = fields.Many2one('stock.warehouse', compute='_compute_warehouse', store=True)

    @api.depends('picking_type_id')
    def _compute_warehouse(self):
        for rec in self:
            rec.warehouse_id = rec.picking_type_id.warehouse_id
            _logger.info("Warehouse computed for picking %s: %s", rec.name or rec.id,
                         rec.warehouse_id.name or rec.warehouse_id.id)

    # @api.model
    # def default_get(self, fields):
    #     res = super().default_get(fields)
    #     if self.env.context.get('default_warehouse_id'):
    #         res['warehouse_id'] = self.env.context['default_warehouse_id']
    #     return res
