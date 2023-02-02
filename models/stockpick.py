from odoo import fields, api, models

class inherit_stock(models.Model):
    _inherit = 'stock.move'


    picking = fields.Char(string='Sale Oder line')

    descc = fields.Char(string='Data')



