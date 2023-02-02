from odoo import models, api, fields

class Studentfee(models.Model):
    _name = 'svistfee.details'
    _description = 'Fee Details Of Students'

    name = fields.Many2one('svist.students', string='Student')
    fees = fields.Float(related='name.fees', string='Total Amount')
    day = fields.Date(string='Pay Date', required='True')
    pay = fields.Integer(string='Amount Paying', required='True')
    due_amount = fields.Float(string="Due Amount", compute='_compute_due_amount')

    def _compute_due_amount(self):
        self.due_amount = self.fees - self.pay
