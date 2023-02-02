# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.tools import float_compare

import datetime
from datetime import datetime, timedelta, date


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.depends_context('force_company')
    @api.depends('product_variant_ids', 'product_variant_ids.standard_price')
    def _compute_standard_price(self, template=None):
        # Depends on force_company context because standard_price is company_dependent
        # on the product_product
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        total_val = []
        filter_date = datetime.now() - timedelta(days=90)
        for template in unique_variants:
            po_obj = self.env['purchase.order.line'].search([
                ('product_tmpl_id', '=', template.id),
                ('create_date', '>=', filter_date)])
            po_list = []
            for po in po_obj:
                po_list.append(po)
            if len(po_list) != 0:
                for po in po_obj:
                    total_val.append(po.price_unit)
                final_val = 0
                if total_val:
                    final_val = sum(total_val) / len(total_val)
                else:
                    final_val = 0
                template.standard_price = final_val
            else:
                template.standard_price = template.standard_price

        # unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        # for template in unique_variants:
        #     template.standard_price = template.product_variant_ids.standard_price
        # for template in (self - unique_variants):
        #     template.standard_price = 0.0
