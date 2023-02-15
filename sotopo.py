from odoo import api, fields, models, _


class po(models.TransientModel):
    _inherit = 'rfq.from.quotation'

    co = fields.Char(string='coustmer reference')

    @api.model
    def default_get(self, fields):
        res = super(po, self).default_get(fields)
        context = dict(self._context or {})
        active_model = context.get('active_model')
        active_id = context.get('active_id')

        SaleOrder = self.env['sale.order']
        order_obj = SaleOrder.browse(active_id)
        res.update({
            'co': order_obj.client_order_ref

        })

        return res
# class purchasebutton(models.Model):
#     _inherit = 'purchase.order'
#
#     def CreateRFQ(self):
#         result = super(po, self).CreateRFQ()
#         res = self.env['rfq.from.quotation'].search([])
#         for rec in res:
#             if self.
#
#         return res