from odoo import fields,models

class Button(models.Model):
    _inherit = 'sale.order'



    # def action_confirm(self):
    #
    #    res = super(Button,self).action_confirm()

       # inv_obj = self.env['account.move']
       # inv_vals = {
       #     'partner_id': self.partner_id.id,
       #     'invoice_line_ids': [(0, 0, {
       #         'product_id': line.product_id.id,
       #         'quantity': line.product_uom_qty,
       #         'price_unit': line.price_unit,
       #         'name': line.name,
       #         'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
       #     }) for line in self.order_line],
       #     # 'sale_id': self.id,
       # }
       # invoice = inv_obj.create(inv_vals)
       # invoice.action_view_invoice()

       # for picking in self.picking_ids:
       #     if picking.state == 'assigned':
       #         picking.button_validate()

       # return res
    # stock.immediate.transfer
    def action_confirm(self):
        res = super(Button,self).action_confirm()
        # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        r = self.env['stock.picking'].search([])
        m= self.env['account.move'].search([])
        print("#######################", self.picking_ids.name)
        for picking in self.picking_ids:
            for i in r:
                if i.state == 'assigned':
                    picking.action_assign()
                    for move in i.move_ids_without_package:
                         move.quantity_done = move.product_uom_qty
                    picking.button_validate()
        for order in self:
            if order.invoice_status == 'to invoice':
                order._create_invoices()
                # for state in m:
                #     if state.state == 'draft':
        invoices = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        if invoices:
            for invoice in invoices:
                invoice.action_post()
        # for action in m:
        #     action.action_post()
        #     order.state = 'done'
                # if self.state == 'sale':
                #     self.create_invoices()
        # if self.state == 'sale':
        #     for order in self:
        #         invoice = self.env['account.move'].create({
        #             'partner_id': order.partner_id.id,
        #             'move_type': 'out_invoice',
        #             'invoice_origin': order.name,
        #             'invoice_date': fields.Date.today(),
        #             'invoice_line_ids': [(0, 0, {
        #                 'product_id': line.product_id.id,
        #                 'quantity': line.product_uom_qty,
        #                 'price_unit': line.price_unit,
        #                 'name': line.name,
        #                 'account_id': line.product_id.categ_id.property_account_income_categ_id.id,
        #             }) for line in order.order_line],
        #         })
        #         invoice.action_post()
        return res
        # for i in r:
        #     i.move_ids_without_package.write({'quantity_done': self.order_line.product_uom_qty})
        #     if i.state == 'assigned':
        #         t.process()
        #         i.button_validate()




        # for k in t:
        #     k.process()
        # for j in m:
        #     j._quantity_done_set()
        # for i in r:
        #     i.button_validate()
        # for i in r:
        #     i.button_validate()
        # button_validate = self.env.ref('sale.view_order_form')
        return res

# class validate(models.Model):
#     _inherit = 'stock.picking'
#
#     def action_confirm(self):
#         res = super(validate,self).action_confirm()
#         for j in self:
#             j.button_validate()
#         return res
#     def button_validate(self):
#         res = super(validate,self).button_validate()
#         for i in self:
#             i.move_ids_without_package.write({'quantity_done': self.order_line.product_uom_qty})

        # picking_ids = self.picking_ids.filtered(lambda picking: picking.state == 'assigned')
        # validate the pickings
        # ref = self.env['stock.picking'].button_validate()
        # r = self.env["stock.immediate.transfer"].process()
        # return res,ref,r
        # create invoice
        # action = self.env.ref('account.action_move_out_invoice_type')
        # result = action.read()[0]
        # result.update({'context': {'default_type': 'out_invoice', 'default_partner_id': self.partner_id.id}})
        # return {'type': 'ir.actions.act_window', 'view_mode': 'form', 'view_type': 'form', 'res_model': 'account.move',
        #         'target': 'current',
        #         'context': {'default_type': 'out_invoice', 'default_partner_id': self.partner_id.id},
        #         'name': 'Create Invoice'},re
