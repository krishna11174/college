from odoo import fields,models

class Materials(models.Model):
    _name = 'svist.materials'
    _description = "Core Branch Materials"

    name = fields.Char(string='Branch')
    branch_materials = fields.Char(string='Material')
    total_materials = fields.Integer(string='Set of Books')
    materials_price = fields.Float(string='Price')
