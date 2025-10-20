from odoo import models, fields, api, _

class ProductProduct_custom(models.Model):
    _inherit = 'product.product'

    lst_price = fields.Float(
        'Sales Price',
        digits='Product Price', inverse='_set_product_lst_price',
        help="The sale price is managed from the product template. Click on the 'Configure Variants' button to set the extra attribute prices.",
        store=True)

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
                value = self.env['uom.uom'].browse(self._context['uom'])._compute_price(product.lst_price, product.uom_id)
            else:
                value = product.lst_price
            value -= product.price_extra
            product.write({'list_price': product.list_price})

    def price_compute(self, price_type, uom=None, currency=None, company=None, date=False):
        company = company or self.env.company
        date = date or fields.Date.context_today(self)

        self = self.with_company(company)
        if price_type == 'standard_price':
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
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
                # we need to add the price from the attributes that do not generate variants
                # (see field product.attribute create_variant)
                # if self._context.get('no_variant_attributes_price_extra'):
                    # we have a list of price_extra that comes from the attribute values, we need to sum all that
                #     price += sum(self._context.get('no_variant_attributes_price_extra'))

            if uom:
                price = product.uom_id._compute_price(price, uom)

            # Convert from current user company currency to asked one
            # This is right cause a field cannot be in more than one currency
            if currency:
                price = price_currency._convert(price, currency, company, date)

            prices[product.id] = price

        return prices