# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import api, fields, models, SUPERUSER_ID, _



class ProductTemplate(models.Model):
    _inherit = 'product.template'

    z_hsn_code = fields.Char("HSN Code")



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    z_driver = fields.Char("Driver Name")
    z_contact = fields.Char("Contact Number")
    z_vehicle = fields.Char("Vehicle Number")
    z_dispatch = fields.Datetime("Dispatch Time")