"""

"""
from odoo import models, fields, api
import datetime
import pdb

class InvreportData(models.Model):

	_inherit = 'inventory.base.report'



	# push_data = fields.Boolean("Push",compute='push_datas',store=True)
	push_data1 = fields.Boolean("Push",compute='push_datas',store=True)






	@api.depends('product_id')
	def  push_datas(self):
		opening_qty = '''
			select 
	                product_id ,
	                ABS(sum(product_qty)) as qty,
	                ABS(sum(value)) as value
	        from 
	                inventory_base_report 
	        where 
	                date < %s and 
	                product_id =%s and
	                (warehouse_id IS NULL or warehouse_id in %s  ) and
	                transaction_types NOT IN  ( 'internal' )

	        group by product_id,warehouse_id

		'''		
		for each_line in self :
			if each_line and not each_line.push_data1:
				# if not each_line.warehouse_id.id:
				# 	pdb.set_trace()
				reportobject = self.env['data.for.reports']
				print("newwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww")
				curr_id = reportobject.search([('product_id','=',each_line.product_id.id),('warehouse_id','=',each_line.warehouse_id.id),('date','=',each_line.date.date())])
				if not curr_id:
					# pdb.set_trace()	
					last_date = each_line.date.date() -datetime.timedelta(days=1)

					opening_value_params = (last_date,each_line.product_id.id,tuple(each_line.warehouse_id.ids,) if each_line.warehouse_id else (0,) )
					self.env.cr.execute(opening_qty,opening_value_params)
					op_res = self.env.cr.dictfetchall()




					vlas_list1={
					'product_id':each_line.product_id.id,
					'uom_id':each_line.product_id.uom_id.id,
					'category_id': each_line.product_id.categ_id.id,
					'product_code': each_line.product_id.default_code,
					'warehouse_id':  each_line.warehouse_id.id if each_line.warehouse_id else 0 ,
					'date':  each_line.date.date(),

					'sys_op_qty': op_res[0]['qty'] if op_res else 0.0,

					'sys_op_value': op_res[0]['value'] if op_res else 0.0,

					'gr_in_qty':  each_line.product_qty if each_line.transaction_types == 'p_receipt' else 0.0,
					'gr_in_value':   each_line.value if each_line.transaction_types == 'p_receipt' else 0.0,

					'grr_out_qty':  each_line.product_qty if each_line.transaction_types == 'p_return' else 0.0,
					'grr_out_val':   each_line.value if each_line.transaction_types == 'p_return' else 0.0,

					'selling_qty':  each_line.product_qty if each_line.transaction_types == 's_shipment' else 0.0,
					'selling_val':   each_line.value if each_line.transaction_types == 's_shipment' else 0.0,

					'consumed_qty':  each_line.product_qty if each_line.transaction_types == 'in' else 0.0,
					'consumed_val':   each_line.value if each_line.transaction_types == 'in' else 0.0,

					'to_in_qty':  each_line.product_qty if each_line.transaction_types == 't_receipt' else 0.0,
					'to_in_val':   each_line.value if each_line.transaction_types == 't_receipt' else 0.0,

					'to_out_qty':  each_line.product_qty if each_line.transaction_types == 't_shipment' else 0.0,
					'to_out_val':   each_line.value if each_line.transaction_types == 't_shipment' else 0.0,

					'variance_qty': each_line.product_qty if each_line.transaction_types == 'positive' else 0.0+ each_line.product_qty if each_line.transaction_types == 'negative' else 0.0,
					'variance_val': each_line.value if each_line.transaction_types == 'positive' else 0.0+ each_line.value if each_line.transaction_types == 'negative' else 0.0,

					'wastage_qty':(-(each_line.product_qty) if each_line.product_qty <0 else each_line.product_qty)if each_line.loss_reasons == 'wasted'  else 0.0,
					'wastage_val':(-(each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons =='wasted' else 0.0, 

					'damaged_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'damaged' else 0.0,
					'damaged_val':(-(each_line.value) if each_line.value else each_line.value) if each_line.loss_reasons == 'damaged' else 0.0,

					'inventory_added_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'inventory_added' else 0.0,
					'inventory_added_val':(-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'inventory_added' else 0.0,

					'inventory_closing_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'closing' else 0.0,
					'inventory_closing_val':(-(each_line.value if each_line.value<0 else each_line.value) if each_line.value<0 else each_line.value)if each_line.loss_reasons == 'closing' else 0.0,

					'expired_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'expired' else 0.0,
					'expired_val':(-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'expired' else 0.0,

					'inventory_sale_qty':(-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty) if each_line.loss_reasons == 'sale' else 0.0,
					'inventory_sale_val':(-(each_line.value) if each_line.value<0 else each_line.value) if each_line.loss_reasons == 'sale' else 0.0,


					'sys_closing_qty': op_res[0]['qty'] if op_res else 0.0 + each_line.product_qty if each_line.transaction_types =='p_receipt' else 0.0+
										each_line.product_qty if each_line.transaction_types =='p_return' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='s_shipment' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='in' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='out' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='t_receipt' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='t_shipment' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='positive' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='wasted' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='damaged' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='closing' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='expired' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='sale' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='inventory_added' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='s_return' else 0.0 +
										each_line.product_qty if each_line.transaction_types =='negative' else 0.0,

					'sys_closing_val': op_res[0]['value'] if op_res else 0.0 + each_line.value if each_line.transaction_types =='p_receipt' else 0.0+
										each_line.value if each_line.transaction_types =='p_return' else 0.0 +
										each_line.value if each_line.transaction_types =='s_shipment' else 0.0 +
										each_line.value if each_line.transaction_types =='in' else 0.0 +
										each_line.value if each_line.transaction_types =='out' else 0.0 +
										each_line.value if each_line.transaction_types =='t_receipt' else 0.0 +
										each_line.value if each_line.transaction_types =='t_shipment' else 0.0 +
										each_line.value if each_line.transaction_types =='positive' else 0.0 +
										each_line.value if each_line.transaction_types =='wasted' else 0.0 +
										each_line.value if each_line.transaction_types =='damaged' else 0.0 +
										each_line.value if each_line.transaction_types =='closing' else 0.0 +
										each_line.value if each_line.transaction_types =='expired' else 0.0 +
										each_line.value if each_line.transaction_types =='sale' else 0.0 +
										each_line.value if each_line.transaction_types =='inventory_added' else 0.0 +
										each_line.value if each_line.transaction_types =='s_return' else 0.0 +
										each_line.value if each_line.transaction_types =='negative' else 0.0,


					}
					new_id =reportobject.create(vlas_list1)
					each_line.write({'push_data1':True})
				else:
					update_qty={}

					
					update_qty = {
						'sys_op_qty':curr_id.sys_op_qty,
						'sys_op_value':curr_id.sys_op_value,
						}
					if each_line.transaction_types == 'p_receipt':
						update_qty={
						'gr_in_qty':  curr_id.gr_in_qty+each_line.product_qty ,
						'gr_in_value':   curr_id.gr_in_value+each_line.value,
						 }
					if  each_line.transaction_types == 'p_return':
						update_qty={
							'grr_out_qty':  curr_id.grr_out_qty+each_line.product_qty ,
							'grr_out_val':   curr_id.grr_out_val+each_line.value ,
							}
					if  each_line.transaction_types == 's_shipment':
						update_qty={
							'selling_qty':  curr_id.selling_qty+each_line.product_qty ,
							'selling_val':   curr_id.selling_val+each_line.value ,
							}

					if  each_line.transaction_types == 'in':
						update_qty={
							'consumed_qty':  curr_id.consumed_qty+each_line.product_qty ,
							'consumed_val':   curr_id.consumed_val+each_line.value ,
							}

					if  each_line.transaction_types == 't_receipt':
						update_qty={
							'to_in_qty':  curr_id.to_in_qty+each_line.product_qty ,
							'to_in_val':   curr_id.to_in_val+each_line.value ,
							}
					if each_line.transaction_types == 't_shipment':
						update_qty={
							'to_out_qty':  curr_id.to_out_qty+each_line.product_qty ,
							'to_out_val':  curr_id.to_out_val+ each_line.value ,
							}

					if each_line.loss_reasons == 'wasted':
						update_qty={
							'wastage_qty': curr_id.wastage_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty,
							'wastage_val': curr_id.wastage_qty+-(each_line.value) if each_line.value<0 else each_line.value,
						}
					if each_line.loss_reasons == 'damaged':
						# print("sjethgwu4twuitjbfsh")
						update_qty = {
							'damaged_qty':curr_id.damaged_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty,
							'damaged_val':curr_id.damaged_val+-(each_line.value) if each_line.value<0 else each_line.value,
						}
					if each_line.loss_reasons == 'inventory_added':
						# print("vvvvio0poppppppppu989789oooooooooo")
						update_qty = {
							'inventory_added_qty':curr_id.inventory_added_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty,
							'inventory_added_val':curr_id.inventory_added_val+-(each_line.value) if each_line.value<0 else each_line.value,
						}
					if each_line.loss_reasons == 'closing':
						update_qty = {
							'inventory_closing_qty':curr_id.inventory_closing_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty,
							'inventory_closing_val':curr_id.inventory_closing_val+-(each_line.value) if each_line.value<0 else each_line.value,
						}
					if each_line.loss_reasons == 'expired':
						update_qty = {
							'expired_qty':curr_id.expired_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty,
							'expired_val':curr_id.expired_val+-(each_line.value) if each_line.value<0 else each_line.value,
						}
					if each_line.loss_reasons == 'sale':
						update_qty = {
							'inventory_sale_qty':curr_id.inventory_sale_qty+-(each_line.product_qty) if each_line.product_qty<0 else each_line.product_qty,
							'inventory_sale_val':curr_id.inventory_sale_val+-(each_line.value) if each_line.value<0 else each_line.value,

						}
					if each_line.transaction_types != 'internal':
						update_qty = {
							'sys_closing_qty':curr_id.sys_closing_qty + each_line.product_qty,
							'sys_closing_val':curr_id.sys_closing_val + each_line.product_qty,
						}


					elif each_line.transaction_types == 'positive' or each_line.transaction_types == 'negative':
						update_qty={
							'variance_qty': curr_id.variance_qty+each_line.product_qty ,
							'variance_val': curr_id.variance_val+each_line.value ,
						}
					curr_id.write(update_qty)
					each_line.write({'push_data1':True})






























