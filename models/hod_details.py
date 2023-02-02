from odoo import models, api, fields

class Hod(models.Model):
    _name = 'svist.hod'
    _description = "About Dept. HOD's"
    _rec_name = "hod_name"

    hod_name = fields.Char(string='Name', required="True")
    hod_exp = fields.Integer(string='Experince', required='True')
    hod_qulification = fields.Char(string='Qualification', required='True')
    hod =fields.Integer(string='Hod Count')
    sir_id = fields.One2many('relation', 'field_id')
    product_id=fields.Many2one('product.template', string='product Template')

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            lines = [(5,0,0)]
            print('/////////////////////////////',self.product_id.product_variant_ids)
            for line in self.product_id.product_variant_ids:
                vals = {
                    'product_id' : line.id,
                'product_qty' : 5

                }

                lines.append((0, 0, vals))
            print('liness', lines)
            rec.sir_id = lines


class relaiononchange(models.Model):
    _name = 'relation'
    _description = 'onchange'

    product_id=fields.Many2one('product.product', string="Sir's")
    product_qty=fields.Integer(string="Quantity")
    field_id=fields.Many2one("svist.hod", string="sir ID")