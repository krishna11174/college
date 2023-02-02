from odoo import models,fields

class admission(models.TransientModel):
    _name = 'admission.student'
    _description = 'student admissions'

    nam = fields.Many2one("svist.students", string="Student Name")