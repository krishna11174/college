from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class PurchaseApprovalMatrixLine(models.Model):
    _name = 'purchase.approval.matrix.line'
    # _rec_name = 'value'

    min_value = fields.Integer(string='Min Value')
    max_value = fields.Integer(string='Max Value')
    user_ids = fields.Many2many('res.users', string="Users")
    po_matrix_id = fields.Many2one('purchase.approval.matrix', string="PO Matrix")


class PurchaseApprovalMatrix(models.Model):
    _inherit = 'purchase.approval.matrix'

    matrix_line = fields.One2many('purchase.approval.matrix.line', 'po_matrix_id', string="Matrix Line")


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    po_approved_by = fields.Many2one('res.users', string="PO Approved By")


    def button_approve(self, force=False):
        cat = self.order_line[0].product_id.categ_id
        approval_ref = self.env['purchase.approval.matrix'].search([
            ('product_category_id', '=', cat.id)])
        approval_ref_line = self.env['purchase.approval.matrix.line'].search([
            ('po_matrix_id', '=', approval_ref.id), ('min_value', '<', self.amount_total),
            ('max_value', '>', self.amount_total)])
        for line in approval_ref_line:
            if approval_ref and line.min_value < self.amount_total < line.max_value and self.env.user not in line.user_ids:
                raise UserError(_('You are not authorized to approve PO of ' + cat.name + ' category'))
        self.write({'state': 'purchase', 'date_approve': fields.Date.context_today(self)})
        self.filtered(lambda p: p.company_id.po_lock == 'lock').write({'state': 'done'})
        self._create_picking()
        return {}

    def button_confirm(self):
        for order in self:
            if order.state not in ['draft', 'sent']:
                continue
            order._add_supplier_to_product()

            cat = order.order_line[0].product_id.categ_id
            current_user = self.env.user
            order.po_approved_by = current_user
            # for line in order.order_line:
            #     if line.product_id.categ_id != cat:
            #         raise UserError(_('Can not confirm an order with products from different Categories'))

            approval_ref = self.env['purchase.approval.matrix'].search([
                ('product_category_id', '=', cat.id)])
            if approval_ref.matrix_line:
                for line in approval_ref.matrix_line:
                    if not approval_ref:
                        order.button_approve()
                        # elif order.amount_total <= approval_ref.value or self.env.user in approval_ref.user_ids:
                    elif line.min_value < order.amount_total < line.max_value or self.env.user in line.user_ids:
                        order.button_approve()
                    else:
                        order.write({'state': 'to approve'})
            else:
                order.button_approve()
        return True

    company_partner = fields.Many2one('company.data', string="Company")
