# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from datetime import date
from odoo import models, fields, api, _


class Svist(models.Model):
    _name = 'svist.students'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Student Detials '

    name = fields.Char(string='Name')
    image =fields.Binary(string= 'student image')
    ref = fields.Char(string='ADM', required=True, readonly=True, copy=False, default=lambda self: _('NEW'))
    adm = fields.Char(string='Admission No.', readonly=True, copy=False, default=lambda self: _('New'))
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')], required=True)
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
    sir_id = fields.Many2one('svist.hod', string='HOD')
    faculty_ids = fields.Many2many('svist.hod', string='Faculties')
    num_of_f = fields.Integer(string="No.of F", compute="_compute_faculty")
    books = fields.Char(string='Materials')
    book_ids = fields.One2many('student.materials', 'student_id', string="Material line")
    faculty = fields.Integer(string="HOD's", compute="compute_hod")

    #  (compute='compute_due_amt')

    # Buttons created for from Status
    # this Object Type buttons

    def button_confirm(self):
        self.state = 'confirm'

    def button_done(self):
        self.state = 'done'

    def button_inprogress(self):
        self.state = 'in_progress'

    def button_draft(self):
        self.state = 'draft'

    def button_cancel(self):
        self.state = 'cancel'

    def search_method(self):
        search = self.env['svist.students'].search([("gender", '=', "male")]).mapped('name')
        # print('...................................................', search)

    # def _compute_due_amount(self):
    #   self.due_amount = self.fees - self.pay
    # Here, Age field is depending on DOB field
    # in this Situation we can use "depends" or "on_change method"

    @api.depends('dob')
    def compute_age(self):
        for rec in self:
            today = date.today()
            if rec.dob:
                t = today.year - rec.dob.year
                rec.age = t
            else:
                rec.age= 0

    # Over Ridding the Cerate Method &&
    # Sequence Generation of Every New Quetation or Every New Student Admission
    # def set_line_no(self):
    #     sl_no=0
    #     for line in self.book_ids:
    #         sl_no+=1
    #         line.sl_no = sl_no
    #     return

    def set_line_number(self):
        sl_no = 0
        for line in self.book_ids:
            sl_no += 1
            line.sl_no = sl_no
        return

    @api.model
    def create(self, vals):
        if vals.get('adm', _('New')) == _('New'):
            vals['adm'] = self.env['ir.sequence'].next_by_code('adm.seq') or _('New')
        res = super(Svist, self).create(vals)
        res.set_line_number()
        return res

    def write(self, vals):
        res = super(Svist, self).write(vals)
        self.set_line_number()
        return res

    def total_due(self):
        # print("test//////////////////////////////")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Due Amt',
            'res_model': 'svist.hod',
            'view_mode': 'from',
            'view_id': self.env.ref('College.hod_detail').id,
            # 'domain': [('hod_name','=',self.sir_id)],
            'target': 'current',
        }

    def button_type_wizard(self):
        view_id = self.env.ref('College.creating_admission_form').id
        lines=[]
        sirs=[]
        for i in self.book_ids:
            lines.append((0,0, {"books_price" : i.books_price,
                                   "books_set" : i.books_set,
                                   "books_ids" :i.books_ids.id}))

        for sir in self.faculty_ids:
            sirs.append((sir.id))
            # sirs.append((6,0,[sir.id]))
        # print(sirs)



        f = self.id
        # print(f)

        # print("@@@@@@@@@@@@@@@@@",lines)
        # n = self._context.get('active_id')
        # print(self.name)
        # print(active_id)
        # for rec in self._context.get('active_id'):
        #     n.append((0,0,{"name": rec.name}))
        # print("@@@@@@@@@@@@@@@@@@@@@",n)
        cxt= {
            'default_name' : self.id,
            'default_book_ids' : lines,
            'default_sir_id' : self.sir_id.id,
            'default_father_name' : self.father_name,
            'default_faculty_ids' : sirs,

        }
        # print(self.name.id)
        return {
            "type": "ir.actions.act_window",
            "name": "Wizard",
            'context': cxt,
            "view_mode": "form",
            "res_model": "studentadm.svist",
            "target": "new",
            "view_id": view_id,
            # "res_id" : self.name,


        }

    def compute_hod(self):
        hod = self.env['svist.hod'].search_count([])
        self.faculty = hod

    # def _compute_faculty(self):
    #     fac = self.env['svist.hod'].search_count(['hod_name', '=', self.faculty_ids])
    #     return fac


# One2many

class Studentmaterials(models.Model):
    _name = 'student.materials'
    _description = "Books for Core Wise"

    books_ids = fields.Many2one('svist.materials', string='Books')
    sl_no = fields.Integer(string='Serial no')
    books_price = fields.Float(String='price', default='600')
    books_set = fields.Float(string='Quntity', default='1')
    student_id = fields.Many2one("svist.students", string="Student")
