from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    batch_number = fields.Char(string="Batch Number")


class StockPickingval(models.Model):
    _inherit = 'stock.picking'

    batch_no = fields.Char(string="Batch Number")
    manufacture_date = fields.Date(string="Mfg Date")
    expiry_date = fields.Date(string="Expiry Date")

    def button_validate(self):
        res = super(StockPickingval, self).button_validate()
        for rec in self:
            for line in rec.move_line_ids_without_package:
                lot_obj = self.env['stock.production.lot'].search([('id', '=', line.lot_id.id)])
                for lot in lot_obj:
                    lot.manufacture_date = line.manufacture_date
                    lot.life_date = line.expiry_date
                    lot.batch_number = line.batch_number
        return res


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    manufacture_date = fields.Datetime(string="Mfg Date")
    expiry_date = fields.Datetime(string="Expiry Date")
    batch_number = fields.Char(string="Batch Number")
    shelf_life = fields.Boolean(string="Shelf Life", default=False)
    shelf_life_pursuable = fields.Boolean(related='product_id.categ_id.shelf_life_pursuable')

    @api.onchange('product_id')
    def onchange_product_id(self):
        for rec in self:
            lot_obj = self.env['stock.production.lot'].search([
                ('product_id', '=', rec.product_id.id)], limit=1)
            rec.lot_id = lot_obj

    @api.onchange('lot_id')
    def onchange_lot_id(self):
        for rec in self:
            if rec.lot_name:
                rec.manufacture_date = rec.lot_id.manufacture_date
                rec.expiry_date = rec.lot_id.life_date
