# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

from datetime import date
from datetime import datetime
from datetime import datetime, timedelta
from odoo.exceptions import UserError, ValidationError
import calendar
import re
import json
from dateutil.relativedelta import relativedelta
import pgeocode
import qrcode
from PIL import Image
from random import choice
from string import digits
import json
import re
import uuid
from functools import partial



class AccountPayment(models.Model):
    _inherit = "account.payment"

    def action_reverse_cash_book(self):
        if self.journal_id.type == 'cash':
            if not self.env['cash.book.info'].search([]):
                # complete = sum(self.env['account.move.line'].search([('journal_id', '=', self.journal_id.id)]).mapped('debit'))
                complete = sum(self.env['account.move.line'].search(
                    [('account_id', '=', self.journal_id.payment_credit_account_id.id)]).mapped('debit'))
            else:
                complete = self.env['cash.book.info'].search([])[-1].balance

            debit = 0
            credit = 0
            complete_new = 0
            acc = self.env['account.account']
            # if self.payment_type == 'outbound':
            credit = self.amount
            complete_new = complete - credit
            acc = self.journal_id.payment_credit_account_id.id
            # if self.payment_type == 'inbound':
            #     debit = self.amount
            #     complete_new = complete - debit
            #     acc = self.journal_id.payment_debit_account_id.id

            self.env['cash.book.info'].create({
                'date': self.date,
                'account_journal': self.journal_id.id,
                'partner_id': self.partner_id.id,
                'company_id': self.company_id.id,
                # 'description': self.communication,
                'description': self.partner_id.name,
                'payment_type': self.payment_type,
                'partner_type': self.partner_type,
                'debit': debit,
                'credit': credit,
                'account': acc,
                'payment_id': self.id,
                'balance': complete_new

            })


