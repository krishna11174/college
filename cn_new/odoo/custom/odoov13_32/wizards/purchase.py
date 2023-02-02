# -*- coding: utf-8 -*-

import logging
from odoo import models
import pdb

_logger = logging.getLogger(__name__)

class POProductPrice(models.TransientModel):
    _name = 'po.product.price'
    _description = "Wizard - po.product.price"



    def get_price(self):
        """filter the records of the state 'draft' ,
        and will confirm this and others will be skipped"""

        quotations = self._context.get('active_ids')
        for each_po in quotations:
            quotations_ids = self.env['purchase.order'].browse(quotations).\
                filtered(lambda x: x.state == 'draft' )
            if quotations_ids:
                for quotation in quotations_ids.order_line:
                    currrent_qty = quotation.product_qty

                    if quotation.product_brand_id:
                        quotation.onchange_product_id()
                    else:
                        quotation._onchange_quantity()


                    quotation.write({
                                    'date_planned':quotation.order_id.date_planned,
                                    'product_qty':currrent_qty})

class PurchaseOrderConfirm(models.TransientModel):
    _name = 'purchase.order.confirm'
    _description = "Wizard - Purchase Order Confirm/Cancel"

    def purchase_confirm(self):
        """filter the records of the state 'draft' and 'sent',
        and will confirm this and others will be skipped"""
        quotations = self._context.get('active_ids')
        quotations_ids = self.env['purchase.order'].browse(quotations).\
            filtered(lambda x: x.state == 'draft' or x.state == "sent")
        for quotation in quotations_ids:
            quotation.button_confirm()

    def purchase_cancel(self):
        quotations = self._context.get('active_ids')
        quotations_ids = self.env['purchase.order'].browse(quotations)
        for quotation in quotations_ids:
            try:
                quotation.button_cancel()
            except:
                pass



    




