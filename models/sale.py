# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields

class SaleInher(models.Model):
    _inherit = 'sale.order'


    sale_description = fields.Char(string='Sale description')

    # def action_confirm(self):
    #
    #     return super(SaleInher, self).action_confirm()
    # def action_confirm(self):
    #     n=self.env['sale.order.line'].browse(['desc'])
    #     for line in n:
    #         print('@@@@@@@@@@@@@@@@@@@',line)
    #     # for line in n:
    #     #     if line == 'desc':
    #     #         p=self.env['stock.move']
    #
    #     return super(SaleInher, self).action_confirm()

class saleorderline(models.Model):
    _inherit = 'sale.order.line'


    desc = fields.Char(string='Data')

    def _prepare_procurement_values(self, group_id=False):
        res = super(saleorderline,self)._prepare_procurement_values(group_id)
        res.update({'desc':self.desc})
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@',self.desc)
        return res
class purchaseorderline(models.Model):
    _inherit = 'purchase.order.line'

    test = fields.Char(string='Data')

    # @api.multi
    def _prepare_stock_moves(self,picking):
        res = super(purchaseorderline,self)._prepare_stock_moves(picking)
        for rec in res:
            rec['test'] =self.test
        return res

class stockruleext(models.Model):
    _inherit = 'stock.rule'


    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):
        res = super(stockruleext,self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values)
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@values',values)
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@product_id',product_id)
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@product_qty',product_qty)
        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@product_uom',product_uom)

        res['descc'] = values.get('desc', False)
        return res

    # @api.model
    def _prepare_purchase_order_line(self, product_id, product_qty, product_uom, company_id, values,supplier, po):
        res =super(stockruleext,self)._prepare_purchase_order_line(product_id, product_qty, product_uom, company_id,values, supplier, po)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@po",po)
        # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@supplier",values)

        res['picking'] = values.get('test', False)
        return res