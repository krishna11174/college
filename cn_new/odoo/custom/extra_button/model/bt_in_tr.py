from odoo import api, fields, models, _


class Button_In_Transfers(models.Model):
    _inherit = "stock.picking"

    @api.depends('state', 'move_ids_without_package')
    def Extra_button(self):
        for l in self:
            tot_grn_val = 0.0
            if l.state == 'done':
                for each_line in l.move_ids_without_package:
                    tax_p = 0.0
                    if each_line.purchase_line_id:
                        tax_p = each_line.purchase_line_id.price_tax / each_line.purchase_line_id.product_qty
                    tot_grn_val += ((each_line.price_unit * each_line.quantity_done) + (
                            tax_p * each_line.quantity_done))
                    print(tot_grn_val)

                l.grn_value = tot_grn_val 

            else:
                for each_line in l.move_ids_without_package:
                    if each_line.purchase_line_id:
                        l.from_po = True
                l.grn_value = tot_grn_val
                print(tot_grn_val)

