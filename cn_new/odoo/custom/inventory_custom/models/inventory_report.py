from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
from datetime import datetime, timedelta


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    avg_consumption = fields.Float(string="Last 30 days consumption", compute='compute_avg_consumption')
    critical_stock = fields.Integer(string="Critical Stock")
    manufacture_date = fields.Datetime(related='lot_id.manufacture_date', string="Mfg Date")
    expiry_date = fields.Datetime(related='lot_id.life_date', string="Expiry Date")
    batch_number = fields.Char(related='lot_id.batch_number', string="Batch Number")

    def compute_avg_consumption(self):
        for rec in self:
            before_month = datetime.now() - timedelta(days=30)
            cons_obj = self.env['inventory.base.report'].search([
                ('transaction_types', '=', 'in'), ('product_id', '=', rec.product_id.id), ('date', '<=', before_month)])
            cons_list = []
            for cons in cons_obj:
                if cons.product_qty:
                    cons_list.append(cons.product_qty)
            sale_obj = self.env['inventory.base.report'].search([
                ('transaction_types', '=', 's_shipment'), ('product_id', '=', rec.product_id.id),
                ('date', '<=', before_month)])
            sale_list = []
            for sale_s in sale_obj:
                if sale_s.product_qty:
                    sale_list.append(sale_s.product_qty)
            sale_tot = sum(sale_list)
            cons_tot = sum(cons_list)
            tot_val = len(sale_list) + len(cons_list)
            if tot_val != 0:
                final_tot = cons_tot + sale_tot / tot_val
                rec.avg_consumption = abs(final_tot)
            else:
                rec.avg_consumption = 0
