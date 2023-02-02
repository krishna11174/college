from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_view_po(self):
        action = self.env.ref('purchase.action_purchase_order_report_all').read()[0]
        action['domain'] = ['&', ('state', 'in', ['purchase', 'done']), ('product_tmpl_id', 'in', self.ids)]
        action['context'] = {
            'graph_measure': 'qty_ordered',
            'search_default_orders': 1,
            'search_default_group_date_approve_3month': 1,
            # 'time_ranges': {'field': 'date_approve'}
            # 'time_ranges': {'field': 'date_approve', 'range': 'last_365_days'}
        }
        return action