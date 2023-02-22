from odoo import http
from odoo.http import request

class student(http.Controller):
    @http.route('/student_details', type='http', auth='public', website='True')
    def stud(self):
        details = request.env['svist.students'].sudo().search([])
        values={
            'details' : details
        }
        # return 'hello krishna'
        return request.render('College.details',values)


class AuthController(http.Controller):
    @http.route('/login', auth='public', type='http', website=True, method=['POST'])
    def login_submit(self):
        return http.local_redirect('/auth/login')

    @http.route('/auth/login', auth='user', website='True')
    def login_form(self):
        return http.request.render('College.login_form')

    @http.route('/login/resuser', type='http',  auth='public', website='True')
    def user_login(self, **kwargs):
        if request.httprequest.method == 'POST':
            name = kwargs.get('name')
            gender = kwargs.get('gender')
            uid = request.session.authenticate(request.env.svist.students, name, gender)
            if uid:
                return http.local_redirect('/student_details')
            else:
                error_msg = "Invalid login or password"
                return http.request.render('College.login_form', {'error': error_msg})
        else:
            return http.request.render('College.login_form')
            # login : kwargs.get('Name')
            # password : kwargs.get('Password')
            # users = request.session.authenticate(request.env.svist.student, login, password)
            # if users:
            #     return http.request.redirect('/student_details')
            # else:
            #     error= 'wrong details'
            #     return http.request.render('College.login_form',{'error':error})
