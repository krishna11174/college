from odoo import models


class PartnerXlsx(models.AbstractModel):
    _name = 'report.college.reports_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, students):
        sheet = workbook.add_worksheet('student details')
        bold = workbook.add_format({'bold': True})
        # One sheet by partner
        row = 0
        col = 0
        sheet.write(row, col, 'Name', bold)
        sheet.write(row, col + 1, 'Branch', bold)
        row += 1
        for objs in students:
            name = objs.name
            bran = objs.branch

            if name == False:
                sheet.set_column('A:A',0)
            else:
                sheet.set_column('A:A', len(name))

            sheet.set_column('B:B', len(bran))

            sheet.write(row, col, name, bold)
            sheet.write(row, col + 1, bran, bold)
            row += 1
