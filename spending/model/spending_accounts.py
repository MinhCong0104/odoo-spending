# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Accounts(models.Model):
    _name = 'spending.accounts'
    _description = 'Spending Accounts'

    name = fields.Char(translate=True, required=True)
    amount_first = fields.Monetary(required=True, readonly=True, default=0)
    amount = fields.Monetary(compute='_compute_amount', currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', required=True)
    is_save = fields.Boolean(default=False, help="This account is use for saving. "
                                                 "You can use regular bank account as savings account.")
    type = fields.Selection()  # sử dụng, tiết kiệm, đầu tư
    transactions_in = fields.One2many('spending.transactions', 'to_account')
    transactions_out = fields.One2many('spending.transactions', 'from_account')
    note = fields.Char()
    user_id = fields.Many2one('res.users')

    # các trường với tài khoản tiết kiệm:

    # các trường với tài khooản đầu tư:

    @api.depends('transactions_in', 'transactions_out')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.amount_first + sum(rec.transactions_in.mapped('amount')) - sum(rec.transactions_out.mapped('amount'))


class SaveAccounts(models.Model):
    """Tài khoản tiết kiệm
    Note: Túi thần tài được coi như tài khoản tiêu dùng bình thường
    Thêm trường: ngày bắt đầu, ngày kết thúc, số tiền mục tiêu
    Sửa phương thức:
    1. Không cho rút tiền ra
    2. Tất toán:
        - Rút ra toàn bộ số tiền hiện có - ghi nhận internal transaction
        - Ghi nhận lãi là thu nhập
    """
    _name = 'spending.accounts.save'
    _inherit = 'spending.accounts'

    date_start = fields.Date(required=True)
    date_end = fields.Date()
    target = fields.Float()

    def withdraw(self):
        # tất toán / rút tiền
        pass

    def deposit(self):
        # gửi tiền
        pass


class InvestAccounts(models.Model):
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
    _name = 'spending.accounts.invest'
    _inherit = 'spending.accounts'

    date_start = fields.Date(required=True)
    liquid_amount = fields.Monetary(currency_field='currency_id')
    asset_amount = fields.Monetary(currency_field='currency_id')
    total = fields.Monetary(currency_field='currency_id', compute="_compute_money")
    rate_profit = fields.Float(compute="_compute_money")

    @api.depends('amount', 'liquid_amount', 'asset_amount')
    def _compute_money(self):
        for rec in self:
            rec.total = rec.liquid_amount + rec.asset_amount
            rec.rate_profit = (rec.total - rec.amount) / rec.amount
        pass

# class UseAccounts(models.Model):
#     _name = 'spending.accounts.use'
#     _inherit = 'spending.accounts'
