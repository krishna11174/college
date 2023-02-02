from odoo import fields,api,models


class Studentwiz(models.TransientModel):
    _name = 'studentadm.svist'
    _description = 'Admission'

    # name = fields.Many2one("svist.students", string='Name', required= True)
    name = fields.Many2one("svist.students", string='Name', required='True')
    # ref = fields.Char(string='ADM', required=True, readonly=True, copy=False, default=lambda self: _('NEW'))
    # adm = fields.Char(string='Admission No.', readonly=True, copy=False, default=lambda self: _('New'))
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], required=True, related='name.gender')
    age = fields.Integer(string='Age', compute='compute_age')
    dob = fields.Date(string='DOB')
    branch = fields.Selection([('eee', 'EEE'),
                               ('ece', 'ECE'),
                               ('civil', 'CE'),
                               ('cse', 'CSE'),
                               ('mech', 'MECH')],
                              string='Select Branch', required=True)
    address = fields.Text(string='Address')
    father_name = fields.Char(string='Father Name')
    mother_name = fields.Char(string='Mother Name')
    fees = fields.Float(string='Fees')
    father_occupation = fields.Char(string='Father Occupation', required=True)
    joining_date = fields.Date(string='D.O.J', required=True)
    state = fields.Selection([('draft', 'Draft'),
                              ('in_progress', 'InProgress'),
                              ('confirm', 'Confirm'),
                              ('cancel', 'Cancel'),
                              ('done', 'Done')], default='draft', string='status')
    sir_id = fields.Many2one('svist.hod', string='HOD', related='name.sir_id')
    faculty_ids = fields.Many2many('svist.hod', string='Faculties')
    num_of_f = fields.Integer(string="No.of F", compute="_compute_faculty")
    books = fields.Char(string='Materials')
    book_ids = fields.One2many('student.materials', 'student_id', string="Material line")
    faculty = fields.Integer(string="HOD's", compute="compute_hod")

    # @api.model
    # def default_get(self,fields):
    #    ids = super(Studentwiz ,self).default_get(fields)
    #    ids['name'] = self._context.get('active_id')
    #    return ids

