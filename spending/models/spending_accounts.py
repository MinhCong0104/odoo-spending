# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Accounts(models.Model):
    _name = 'spending.accounts'
    _description = 'Spending Accounts'

    name = fields.Char(translate=True, required=True)
    amount = fields.Monetary(currency_field='currency_id', compute='_compute_amount')
    currency_id = fields.Many2one("res.currency", string='Currency', default=lambda self: self.env.company.currency_id)
    type = fields.Selection([('use', 'Use'), ('save', 'Save'), ('invest', 'Invest')], default='use', required=True)
    note = fields.Text()
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    rate = fields.Float(compute="_compute_rate", store=True, readonly=False)
    date_start = fields.Date()
    # với tài khoản tiết kiệm (biết lãi suất và ngày rút):
    date_end = fields.Date()
    target = fields.Float()
    # với tài khoản đầu tư (chưa biết lãi suất và ngày rút):
    amount_now = fields.Monetary(currency_field='currency_id')

    # phương thức tính số tiền trong tài khoản
    def _compute_amount(self):
        query = f"""
            SELECT COALESCE(SUM(amount), 0) AS amount
            FROM spending_transactions
            WHERE %(account)s = %(account_id)s
        """
        for rec in self:
            self.env.cr.execute(query % {'account': 'to_account', 'account_id': rec.id})
            amount_in = self.env.cr.dictfetchone()['amount']
            self.env.cr.execute(query % {'account': 'from_account', 'account_id': rec.id})
            amount_out = self.env.cr.dictfetchone()['amount']
            rec.amount = amount_in - amount_out

    # phương thức tính tỷ suất lợi nhuận (%/năm) đối với tk đầu tư

    # Methods đối với tài khoản tiết kiệm
    """Tài khoản tiết kiệm
    Sửa phương thức:
    1. Không cho rút tiền ra
    2. Tất toán:
        - Rút ra toàn bộ số tiền hiện có - ghi nhận internal transaction
        - Ghi nhận lãi là thu nhập
    """
    def withdraw(self):
        # tất toán / rút tiền
        # mở wizard cho nhập tổng số tiền (default=target), chọn tài khoản nhận tiền
        # tạo 1 bút toán internal, 1 bút toán income
        pass

    @api.depends('amount', 'amount_now')
    def _compute_rate(self):
        for rec in self:
            if rec.type == 'invest':
                if rec.amount == 0:
                    rec.rate = 0
                else:
                    rec.rate = (rec.amount_now - rec.amount) / rec.amount

