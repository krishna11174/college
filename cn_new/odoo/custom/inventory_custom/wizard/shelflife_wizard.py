from odoo import models, fields, api, _


class ShelflifeWarning(models.TransientModel):
    _name = 'shelflife.warning'

    name = fields.Char(string="Name")
    picking_id = fields.Many2one('stock.picking', "Picking")
    move_id = fields.Many2one('stock.move.line',"Move")

    def shelf_ok(self):
        for rec in self:
            if rec.picking_id:
                if rec.move_id:
                    rec.move_id.shelf_life = True

