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
SELECT COALESCE(SUM(), 0)
FROM spending_transactions
WHERE from_account = %(from_account)s
"""

    # phương thức tính tỷ suất lợi nhuận (%/năm) đối với tk đầu tư

    # Methods đối với tài khoản tiết kiệm
    """Tài khoản tiết kiệm
    Note: Túi thần tài được coi như tài khoản tiêu dùng bình thường
    Thêm trường: ngày bắt đầu, ngày kết thúc, số tiền mục tiêu
    Sửa phương thức:
    1. Không cho rút tiền ra
    2. Tất toán:
        - Rút ra toàn bộ số tiền hiện có - ghi nhận internal transaction
        - Ghi nhận lãi là thu nhập
    """
    def withdraw_all(self):
        # tất toán / rút tiền
        # mở wizard cho nhập số tiền lãi (default=target-amount), chọn tài khoản nhận tiền
        # Create 2 transactions:
        # 1. Internal transaction: amount = số tiền đã gửi, type = internal
        # 2. Income: amount = số lãi nhập vào
        pass

    def deposit(self):
        # gửi tiền
        pass

    # Methods đối với tài khoản đầu tư
    """Tài khoản đầu tư
    Thêm trường: total, liquid_amount, asset_amount, start_date, amount_profit, rate_profit, rate_profit_per_year
        total: số tiền hiện tại, amount: số tiền tươi nạp vào
        total = liquid_amount + asset_amount
        amount_profit = total - amount
        rate_profit = amount_profit / amount * 100%
        rate_profit_per_year: chuyển đổi lợi nhuận theo %/năm
    Sửa phương thức:
    1. Thêm điều kiện khi rút tiền ra: không được rút quá liquid_amount
    """
    @api.depends('amount', 'liquid_amount', 'asset_amount')
    def _compute_money(self):
        for rec in self:
            if rec.type == 'invest':
                rec.total = rec.liquid_amount + rec.asset_amount
                if rec.amount == 0:
                    rec.rate_profit = 0
                else:
                    rec.rate_profit = (rec.total - rec.amount) / rec.amount
            else:
                rec.total = rec.amount
                rec.rate_profit = None
        pass

    def withdraw(self):
        # rút tiền
        # mở wizard cho nhập số tiền muốn rút, chọn tài khoản nhận tiền
        # số tiền rút được < liquid_amount
        pass
