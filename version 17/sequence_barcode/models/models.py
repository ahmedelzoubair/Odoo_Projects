# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SequenceBarcodeProduct(models.Model):
    _inherit = 'product.template'

    @api.model
    def create(self,vals):
        vals['barcode'] = self.env['ir.sequence'].next_by_code('sequence.barcode')
        return super(SequenceBarcodeProduct, self).create(vals)

class SequenceBarcodeVariants(models.Model):
    _inherit = 'product.product'

    @api.model
    def create(self,vals):
        vals['barcode'] = self.env['ir.sequence'].next_by_code('sequence.barcode')
        return super(SequenceBarcodeVariants, self).create(vals)

