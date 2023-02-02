# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _


class StockLocation(models.Model):
	_inherit = "stock.indent.order"

	@api.model
	def create(self,vals):
		res = super(StockLocation,self).create(vals)
		product_list = []
		for rec in res.product_lines:
			if (rec.product_id,rec.product_uom) in product_list:
				raise ValidationError(_("Product %s can't be duplicated") % rec.product_id.name)
			else:
				product_list.append((rec.product_id,rec.product_uom))


		return res

	def write(self,vals):
		res = super(StockLocation,self).write(vals)
		product_list = []
		for rec in self.product_lines:
			if (rec.product_id,rec.product_uom) in product_list:
				raise ValidationError(_("Product %s can't be duplicated") % rec.product_id.name)
			else:
				product_list.append((rec.product_id,rec.product_uom))

		return res