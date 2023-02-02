from odoo import models, fields, api, _,tools
from datetime import timedelta
from num2words import num2words
from qrcode.main import QRCode
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError, AccessError
from datetime import date, datetime
import logging

class PickingoperationLudo(models.Model):
    _inherit = 'stock.picking'

    # def _get_default_currency_id(self):
    #     return self.env.company.currency_id.id


    # currency_id = fields.Many2one('res.currency', string='Currency', compute=_get_default_currency_id)


    # def compute_num2words(self, amount):
    #     print("\n"*25,amount)
    #     return num2words(amount, lang='en').lower()
    #     # return num2words(amount, to = 'currency-In')
    #     # return num2words(amount, lang='en-IN')


    
        
    # def amount_to_text(self, amount):
    #     print("\n"*5, "Im in")
    #     self.ensure_one()
    #     print("\n"*5,"Im 2")
    #     def _num2words(number, lang):
    #         print("\n"*5,"Im 3")
    #         try:
    #             return num2words(number, lang=lang).title()
    #         except NotImplementedError:
    #             return num2words(number, lang='en').title()

    #     print("\n"*5, "Im 4")
    #     if num2words is None:
    #         logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
    #         return ""

    #     print("\n"*5,"Im 5")
    #     formatted = "%.{0}f".format(self.env.company.currency_id.id.decimal_places) % amount
    #     print("\n"*50, formatted)
    #     parts = formatted.partition('.')
    #     integer_value = int(parts[0])
    #     fractional_value = int(parts[2] or 0)

    #     lang = tools.get_lang(self.env)
    #     amount_words = tools.ustr('{amt_value} {amt_word}').format(amt_value=_num2words(integer_value, lang=lang.iso_code), amt_word=self.currency_id.currency_unit_label,).replace(self.currency_id.currency_unit_label,' ').replace(' And ', ' ').replace(',',' ') + ' Only'
    #     if not self.env.company.currency_id.id.is_zero(amount - integer_value):
    #         amount_words += ' ' + _('and') + tools.ustr(' {amt_value} {amt_word}').format(amt_value=_num2words(fractional_value, lang=lang.iso_code),amt_word=self.currency_id.currency_subunit_label,) + ' Only'
    #     return amount_words



