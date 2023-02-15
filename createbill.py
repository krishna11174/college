from odoo import api, fields, models, _

class PicknngId(models.Model):
    _inherit = 'account.move'
    grn = fields.Char(string='GRN number')
    customer_reference_account = fields.Char(string='Coustmer Referenc')


class Stock(models.Model):
    _inherit = "stock.picking"

    number = fields.Integer(string = "Vendor Invoice Number")
    date = fields.Date(string="Vendor Invoice Date")
    customer_reference = fields.Char(string='Customer Reference')

    product=fields.Char(string='Product Name',related='move_ids_without_package.product_id.name')
    quantity_1=fields.Integer(string='Quantity')


class purchase(models.Model):
    _inherit = "purchase.order"

    gn = fields.Char(string='GRN')
    coustmer_refff=fields.Char(string='Coustmer Referenc')

    # def _compute_product_name(self):
    #     stock=self.env['stock.move']
    #     for move in stock:
    #         if move.product_id:
    #             self.product_name = move.product_id.name

# invoice modify or updating new fields on clicking create bill

    def action_view_invoice(self):
        res = super(purchase, self).action_view_invoice()
        m = self.env['stock.picking'].search([])
        for rec in m:
            for recor in rec:
                if self.name == recor.origin:
                    self.gn = recor.name
        res['context']['default_grn']=self.gn
        res['context']['default_customer_reference_account']=self.coustmer_refff
        return res

    def action_view_picking(self):
        res = super(purchase,self).action_view_picking()
        res['default_customer_reference']= self.coustmer_refff
        # res['default_product'] = self.produt_name
        return res
# here the values are updating from purchase.order to stock.picking

    @api.model
    def _prepare_picking(self):
        res = super(purchase,self)._prepare_picking()
        res['costmer_referr'] = self.coustmer_refff
        # res['product']=self.product_id.id.name
        # res['quantity_1'] = self.order_line.product_qty
        return res
