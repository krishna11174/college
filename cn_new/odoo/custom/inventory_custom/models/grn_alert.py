from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
from datetime import datetime


class ProductCategory(models.Model):
    _inherit = 'product.category'

    shelf_life_pursuable = fields.Boolean(string="Shelf Life Pursuable", default=True)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shelf_life_validated = fields.Boolean(string="Shelf Life Validated", default=False,
                                          compute='compute_shelf_life_validated')

    def compute_shelf_life_validated(self):
        for rec in self:
            shelf_val = []
            for line in rec.move_line_ids_without_package:
                shelf_val.append(line.shelf_life)
            if False in shelf_val:
                rec.shelf_life_validated = False
            else:
                rec.shelf_life_validated = True

    def edit_shelf_life(self):
        for line in self.move_line_ids_without_package:
            line.shelf_life = False

    def button_validate_shelf_life(self):
        for rec in self:
            tot_grn_val = 0.0
            for each_line in rec.move_ids_without_package:
                tax_p = 0.0
                if each_line.purchase_line_id:
                    tax_p = each_line.purchase_line_id.price_tax / each_line.purchase_line_id.product_qty
                tot_grn_val += (
                        (each_line.price_unit * each_line.quantity_done) + (tax_p * each_line.quantity_done))
            rec.grn_value = tot_grn_val
            po_obj = self.env['purchase.order'].search([('name', '=', rec.origin)])
            product_list = []
            for line in rec.move_line_ids_without_package.filtered(lambda line: not line.shelf_life):
                if line.product_id.categ_id.shelf_life_pursuable:
                    if not line.batch_number and not line.manufacture_date and not line.expiry_date:
                        product_list.append(line.product_id.default_code)
                        # product_list.append(line.product_id.display_name)
                        # raise ValidationError(_("Please enter the Batch Number,Manufacture Date and Expiry Date"))
            if len(product_list) != 0:
                raise ValidationError(
                    f"Please enter the Batch Number,Manufacture Date and Expiry Date for the mentioned products - {product_list}")
            else:
                for line in rec.move_line_ids_without_package.filtered(lambda line: not line.shelf_life):
                    if line.product_id.categ_id.shelf_life_pursuable:
                        if line.manufacture_date > fields.Datetime.now():
                            raise ValidationError(
                                f"Please enter valid manufacture date - {line.product_id.display_name}:{round(line.qty_done, 3)}{line.product_uom_id.name}/{line.manufacture_date}")
                        if line.expiry_date <= fields.Datetime.now():
                            raise ValidationError(
                                f"Please enter valid expiry date - {line.product_id.display_name}:{round(line.qty_done, 3)}{line.product_uom_id.name}/{line.expiry_date}")
                        else:
                            current_date = datetime.today()
                            date_percentage = 0
                            if line.manufacture_date and line.expiry_date:
                                manuf_date = line.expiry_date - current_date
                                exp_date = line.expiry_date - line.manufacture_date
                                if abs(exp_date).days < 2:
                                    raise ValidationError(
                                        f'Minimum shelf life allowed is 2 days! - {line.product_id.display_name}:{round(line.qty_done, 3)}{line.product_uom_id.name}')
                                date_val = manuf_date / exp_date
                                date_percentage = abs(date_val) * 100
                            if not line.shelf_life:
                                if 30 > date_percentage:
                                    if self.env.user == po_obj.po_approved_by:
                                        view = self.env.ref('inventory_custom.shelflife_warning_form')
                                        return {
                                            'name': _('Shelf Life Warning'),
                                            'type': 'ir.actions.act_window',
                                            'view_type': 'form',
                                            'view_mode': 'form',
                                            'res_model': 'shelflife.warning',
                                            'views': [(view.id, 'form')],
                                            'view_id': view.id,
                                            'target': 'new',
                                            'context': {'default_picking_id': rec.id, 'default_move_id': line.id,
                                                        'default_name': f"Shelf Life period is less than 30% for {line.product_id.display_name}:{round(line.qty_done, 3)}{line.product_uom_id.name}. Are you ready to proceed?"}
                                        }
                                    else:
                                        raise ValidationError(
                                            _(f"Access Denied. Please contact the responsible person(PO "
                                              f"Approved By - {po_obj.po_approved_by.name})."))
                                elif 30 <= date_percentage <= 80:
                                    # if self.env.user == po_obj.po_approved_by:
                                    view = self.env.ref('inventory_custom.shelflife_warning_form')
                                    return {
                                        'name': _('Shelf Life Warning'),
                                        'type': 'ir.actions.act_window',
                                        'view_type': 'form',
                                        'view_mode': 'form',
                                        'res_model': 'shelflife.warning',
                                        'views': [(view.id, 'form')],
                                        'view_id': view.id,
                                        'target': 'new',
                                        'context': {'default_picking_id': rec.id, 'default_move_id': line.id,
                                                    'default_name': f"Shelf Life period is between 30% to 80% for {line.product_id.display_name}:{round(line.qty_done, 3)}{line.product_uom_id.name}. Are you ready to proceed?"
                                                    }
                                    }
                                else:
                                    line.shelf_life = True
                            else:
                                line.shelf_life = True


class StockMove(models.Model):
    _inherit = 'stock.move.line'

    is_filled = fields.Boolean(string="Values updated", compute='compute_values_updated', default=False)

    def compute_values_updated(self):
        for rec in self:
            if not rec.batch_number and not rec.manufacture_date and not rec.expiry_date:
                rec.is_filled = False
            else:
                rec.is_filled = True

    @api.onchange('qty_done')
    def onchange_qty_done(self):
        for rec in self:
            rec.shelf_life = False
