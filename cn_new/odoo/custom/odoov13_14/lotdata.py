from odoo import models, fields, api
from datetime import date


class LotData(models.Model):
	_inherit='stock.inventory.line'

	# eol = fields.Char(string='End of Life', compute="get_lot_data")
	eol = fields.Date(string='End of Life', compute="get_lot_eol")
	mfg = fields.Date(string='Date of Manufacture', compute="get_lot_mfg")
	loss_reason = fields.Selection([('Expired','Expired'),
									('Wasted','Wasted'),
									('Damaged','Damaged'),
									('Inventory Added','Inventory Added'),
									('Sale','Sale')],"Loss Reason", store=True)                          
	@api.depends('prod_lot_id')
	def get_lot_eol(self):
		for l in self:
			if l.prod_lot_id:
				l.eol=l.prod_lot_id.life_date
			else:
				l.eol=""

	def get_lot_mfg(self):
		for l in self:
			if l.prod_lot_id:
				l.mfg=l.prod_lot_id.manufacture_date
			else:
				l.mfg=""
			
	
	
	

