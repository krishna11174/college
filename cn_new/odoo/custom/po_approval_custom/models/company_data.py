from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError


class CompanyData(models.Model):
    _name = 'company.data'

    name = fields.Char(string="Company Name")
    gst_no = fields.Char(string="GST Number")
    logo = fields.Binary(string="Logo")
    street = fields.Char('Street')
    street2 = fields.Char('Street2')
    zip = fields.Char('Zip', change_default=True)
    city = fields.Char('City')
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')
