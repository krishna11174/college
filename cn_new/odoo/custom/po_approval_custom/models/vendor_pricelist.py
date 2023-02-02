from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    product_code = fields.Char(string="Product Code", related='product_tmpl_id.default_code')
    product_name = fields.Char(string="Product", related='product_tmpl_id.name')


# class ProductTemplate(models.Model):
#     _inherit = "product.template"
#
#     def name_get(self):
#         # Prefetch the fields used by the `name_get`, so `browse` doesn't fetch other fields
#         self.browse(self.ids).read(['name', 'default_code'])
#         return [(template.id, template.name) for template in self]
#         # return [(template.id, '%s%s' % (template.default_code and '[%s] ' % template.default_code or '', template.name))
#         #         for template in self]
