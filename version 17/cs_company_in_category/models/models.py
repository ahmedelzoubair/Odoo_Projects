# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit = 'product.category'

    custom_company_id = fields.Many2many(
        'res.company',
        string='Company',
        index=True,
        help="Indicates the company this category belongs to."
    )

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        """
        Override search to filter categories based on user's allowed companies.
        Users can only see categories that belong to companies they have access to,
        or categories with no company assigned (global categories).
        """
        # Get the current user's allowed companies
        user_allowed_companies = self.env.user.company_ids.ids
        
        # Add domain to filter categories based on user's allowed companies
        # Categories with no company (False) should be visible to everyone
        company_domain = ['|', 
                         ('custom_company_id', '=', False),
                         ('custom_company_id', 'in', user_allowed_companies)]
        
        # Combine with existing args
        args = args + company_domain
        
        return super(ProductCategory, self).search(args, offset=offset, limit=limit, order=order)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def search(self, args, offset=0, limit=None, order=None):
        """
        Filter products based on their category's company assignment.
        Users can only see products whose categories belong to their allowed companies.
        """
        # Get the current user's allowed companies
        user_allowed_companies = self.env.user.company_ids.ids

        # Add a domain to filter products based on the category's custom_company_id
        category_company_domain = ['|',
                                 ('categ_id.custom_company_id', '=', False),
                                 ('categ_id.custom_company_id', 'in', user_allowed_companies)]
        
        # Combine with existing args
        args = args + category_company_domain

        return super(ProductTemplate, self).search(args, offset=offset, limit=limit, order=order)


