# -*- coding: utf-8 -*-
from cryptography.utils import read_only_property

from odoo import models, fields, api


# At the below we will add (confirmed_user_id) field at sale pivot report (Sales => Reporting => Sales => Pivot view)
class SaleReport(models.Model):
    _inherit = 'sale.report'  # (addons => sale => report => sale_report.py)
    """
        If you try to open pivot view and make minimise to all Total from Life and Top you will see Untaxed Total number.
     at (+)Total in the right => Add Custom Group => at Lines you will not get our (confirmed_user_id) field
    """

    confirmed_user_id = fields.Many2one('res.users', string="Confirmed User", readonly=True)
    # After adding field her will appears, But if selected error (colum confirmed_user_id does not exist)

    # So now we will inherit Select statement as sale_margin (addons => sale_margin => report => sale_report.py)
    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        # with_clause: Used for any SQL WITH clause required in the query. This can be used to define common table expressions (CTEs).
        # fields: A dictionary where key-value pairs define the additional fields that should be selected in the query.
        # groupby: Specifies the fields to group by in the SQL query, which affects how the pivot table aggregates the data.
        # from_clause: Used for adding any custom FROM clauses or joins to the query.
        fields['confirmed_user_id'] = ", s.confirmed_user_id"
        # Adding my new field to the _query, s => representing to sale_order, Note:- get it from Form statement

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)

    # The below is the new way that add margin,
    # def _select_additional_fields(self, fields):
    #     fields['confirmed_user_id'] = ", s.confirmed_user_id"
    #     return super()._select_additional_fields(fields)



