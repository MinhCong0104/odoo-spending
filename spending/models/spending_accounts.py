# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


TYPES_SELECTION = [('spend', 'Spend'), ('income', 'Income'), ('save', 'Save')]  # sử dụng, tiết kiệm, đầu tư


_logger = logging.getLogger(__name__)


class Accounts(models.Model):
    _name = 'spending.accounts'
    _description = 'Spending Accounts'

    name = fields.Char(translate=True, required=True)
    amount_first = fields.Monetary(required=True, default=0)
    amount = fields.Monetary(compute='_compute_amount', currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', required=True)
    is_save = fields.Boolean(default=False, help="This account is use for saving. "
                                                 "You can use regular bank account as savings account.")
    type = fields.Selection([('use', 'Use'), ('save', 'Save'), ('invest', 'Invest')], required=True)   # sử dụng, tiết kiệm, đầu tư
    default_spend = fields.Boolean()
    transactions_in = fields.One2many('spending.transactions', 'to_account')
    transactions_out = fields.One2many('spending.transactions', 'from_account')
    note = fields.Text()
    user_id = fields.Many2one('res.users')

    # các trường với tài khoản tiết kiệm:
    date_start = fields.Date()
    date_end = fields.Date()
    target = fields.Float()
    account_withdraw = fields.Many2one('spending.accounts')

    # các trường với tài khooản đầu tư:
    liquid_amount = fields.Monetary(currency_field='currency_id')
    asset_amount = fields.Monetary(currency_field='currency_id')
    total = fields.Monetary(currency_field='currency_id', compute="_compute_money")
    rate_profit = fields.Float(compute="_compute_money")

    @api.depends('transactions_in', 'transactions_out')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.amount_first + sum(rec.transactions_in.mapped('amount')) - sum(rec.transactions_out.mapped('amount'))

    def write(self, vals):
        if vals.get('default_spend'):
            if self.type != 'use':
                raise UserError(_('You cannot set an account not for using to default spending account'))
            all_accounts = self.env['spending.accounts'].sudo().search([('user_id', '=', self.env.uid)])
            all_accounts.default_spend = False
        return super(Accounts, self).write(vals)


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
