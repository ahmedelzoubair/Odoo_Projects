from odoo import models, fields, api, _


class ProductTemplateCustom(models.Model):
    _inherit = 'product.template'

    lot_valuated = fields.Boolean('Lot Valuated')


class ProductProductCustom(models.Model):
    _inherit = 'product.product'

    lot_valuated = fields.Boolean('Lot Valuated', related='product_tmpl_id.lot_valuated', store=True)
    lst_price = fields.Float(
        'Sales Price',
        digits='Product Price', inverse='_set_product_lst_price',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.",
        store=True
    )

    @api.depends('list_price', 'price_extra')
    @api.depends_context('uom')
    def _compute_product_lst_price(self):
        to_uom = None
        if 'uom' in self._context:
            to_uom = self.env['uom.uom'].browse(self._context['uom'])

        for product in self:
            if to_uom:
                list_price = product.uom_id._compute_price(product.list_price, to_uom)
            else:
                list_price = product.lst_price
            product.lst_price = list_price

    @api.onchange('lst_price')
    def _set_product_lst_price(self):
        for product in self:
            if self._context.get('uom'):
                value = self.env['uom.uom'].browse(self._context['uom'])._compute_price(product.lst_price,
                                                                                        product.uom_id)
            else:
                value = product.lst_price
            value -= product.price_extra
            product.write({'list_price': product.list_price})

    def price_compute(self, price_type, uom=None, currency=None, company=None, date=False):
        company = company or self.env.company
        date = date or fields.Date.context_today(self)

        self = self.with_company(company)
        if price_type == 'standard_price':
            self = self.sudo()

        prices = dict.fromkeys(self.ids, 0.0)
        for product in self:
            price = product[price_type] or 0.0
            price_currency = product.currency_id
            if price_type == 'standard_price':
                price_currency = product.cost_currency_id

            if price_type == 'list_price':
                price = product.lst_price
                if price == 0:
                    price = product.list_price

            if uom:
                price = product.uom_id._compute_price(price, uom)

            if currency:
                price = price_currency._convert(price, currency, company, date)

            prices[product.id] = price

        return prices
