from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tools import float_compare, float_is_zero
import datetime
from datetime import datetime, timedelta, date


class InventoryMatrixLine(models.Model):
    _name = 'inventory.matrix.line'

    min_value = fields.Integer(string='Min Value')
    max_value = fields.Integer(string='Max Value')
    user_ids = fields.Many2many('res.users', string="Users")
    inventory_matrix_id = fields.Many2one('inventory.matrix', string="PO Matrix")


class InventoryMatrix(models.Model):
    _name = 'inventory.matrix'

    name = fields.Char(string="Name")
    product_category_id = fields.Many2one('product.category', string="Product Category")
    matrix_line = fields.One2many('inventory.matrix.line', 'inventory_matrix_id', string="Matrix Line")


class StockInventoryLine(models.Model):
    _inherit = 'stock.inventory.line'

    unit_price = fields.Float(string="Unit Price", related='product_id.standard_price')
    price_val = fields.Float(string="Difference Price", compute='compute_price_val')
    old_price_val = fields.Float(string="Value", compute='compute_price_old_val')
    month_val = fields.Float(string="Monthly Value", compute='compute_price_monthly_value')

    def compute_price_monthly_value(self):
        for rec in self:
            month_date = datetime.now() - timedelta(days=30)
            inv_obj = self.env['stock.inventory.line'].search([
                ('location_id', '=', rec.location_id.id),
                ('inventory_date', '>=', month_date)])
            inv_list = []
            for inv in inv_obj:
                inv_list.append(inv.price_val)
            tot_val = sum(inv_list)
            if tot_val:
                rec.month_val = tot_val
            else:
                rec.month_val = 0

    def compute_price_old_val(self):
        for rec in self:
            rec.old_price_val = rec.unit_price * rec.theoretical_qty

    def compute_price_val(self):
        for rec in self:
            diff_qty = rec.difference_qty
            rec.price_val = rec.unit_price * (diff_qty if diff_qty > 0 else diff_qty * -1)

    # @api.onchange('product_qty', 'loss_reason')
    # def onchange_loss_reason(self):
    #     for rec in self:
    #         if rec.product_qty > rec.theoretical_qty:
    #             if rec.loss_reason != 'inventory_added':
    #                 raise ValidationError(_("Sorry,You can't add the counted qty more than the onhand qty!"))


class StockInventory(models.Model):
    _inherit = 'stock.inventory'

    def action_validate(self):
        if not self.exists():
            return
        self.ensure_one()
        if not self.user_has_groups('stock.group_stock_manager'):
            raise UserError(_("Only a stock manager can validate an inventory adjustment."))
        if self.state != 'confirm':
            raise UserError(_(
                "You can't validate the inventory '%s', maybe this inventory " +
                "has been already validated or isn't ready.") % (self.name))
        for line in self.line_ids:
            if line.difference_qty:
                if not line.loss_reason:
                    raise UserError(_("Please provide the loss reasons to validate the inventory"))
                else:
                    self.product_ids += line.product_id
                if line.loss_reason == 'expired':
                    if not line.product_id.categ_id.shelf_life_pursuable:
                        raise ValidationError(f"Invalid Loss Reason - Expiry.\n Shelf life is not activated for the "
                                              f"product category {line.product_id.categ_id.name}")
                    if line.difference_qty > 0:
                        raise ValidationError(
                            f"You cannot add quantity with Loss Reason as Expired! {line.product_id.display_name}")
       # if self.env['inventory.matrix'].search([], limit=1):
            # tot_price_val = sum(self.line_ids.mapped('price_val'))
        #    tot_price_val = sum(self.line_ids.mapped('month_val'))
         #   approval_ref_line = self.env['inventory.matrix.line'].search([
          #      ('min_value', '<', tot_price_val),
           #     ('max_value', '>=', tot_price_val)
           # ], limit=1)
           # if approval_ref_line.min_value < tot_price_val <= approval_ref_line.max_value and self.env.user not in approval_ref_line.user_ids:
            #    raise UserError(
             #       f"You are not authorized to approve the inventory \n Allowed approvers - {approval_ref_line.user_ids.mapped('name')}")
        return super(StockInventory, self).action_validate()
