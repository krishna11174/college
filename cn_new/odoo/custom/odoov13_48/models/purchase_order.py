# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from odoo import api, models, fields, _
from odoo.exceptions import AccessError, UserError, ValidationError



class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def check_receipt_date(self):
        today = fields.Date.today()
        for po in self.search([('state', '!=', 'cancel')]):
            if po.date_planned and datetime.date(po.date_planned) + timedelta(days=+2) < today:
                pickings = po.picking_ids.filtered(lambda p: p.state != 'done')
                if not pickings.backorder_id:
                    if pickings and len(po.picking_ids) == 1:
                        pickings.mapped('move_lines').write({'state': 'cancel'})
                        pickings.action_cancel()
                        po.button_cancel()
                    elif pickings:
                        pickings.mapped('move_lines').write({'state': 'cancel'})
                        pickings.action_cancel()
class StockMOveInherit(models.Model):
    _inherit = "stock.move"

    def _set_quantities_to_reservation(self):
        print(222222222222222222222222222222222222222222222)
        for move in self:
            # if move.state not in ('partially_available', 'assigned'):
            #     continue
            for move_line in move.move_line_ids:
                print(33333333333333333333333333333333333333333)
                if move.has_tracking != 'none' and not (move_line.lot_id or move_line.lot_name):
                    continue
                move_line.qty_done = move_line.product_uom_qty
                print(move_line.qty_done,444444444444444444444444444444444444444)



class StockPicking(models.Model):
    _inherit='stock.picking'

    def button_validate(self):
        res=super(StockPicking,self).button_validate()
        if self.purchase_id and not self.message_attachment_count:
            raise UserError(_('Attachment is missing'))
        return res 



class StockPickingResPO(models.Model):
    _inherit='stock.picking'

    def button_validate(self):
        # raise UserError(self and self.origin)
        if self.purchase_id:
            res=super(StockPickingResPO,self).button_validate()
            product_names = ','.join(self.move_ids_without_package.filtered(lambda x:not x.purchase_line_id).mapped('product_id.name'))    
            if product_names:
                raise UserError(_('These [{}] are not allowed to select'.format(product_names)))

            for rec in self.move_ids_without_package:
                if round(rec.quantity_done,3) > rec.product_uom_qty:
                # if rec.product_uom_qty > rec.purchase_line_id.product_qty or rec.product_uom_qty < rec.quantity_done or:
                    raise UserError(_('Demand quantity and Done quantity is not same:'+rec.product_id.name+'('+str(rec.product_uom_qty)+'-'+str(round(rec.quantity_done,3))))
            return res
        else:
            res=super(StockPickingResPO,self).button_validate()
            return res 


    def action_set_quantities_to_reservation(self):
        print(1111111111111111111111111111111111111111111111)
        self.move_lines._set_quantities_to_reservation()




# class purchaseorder():

#     def Purchase_order():







                    
