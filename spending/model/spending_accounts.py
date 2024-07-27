# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


# class Accounts(models.Model):
#     _name = 'spending.accounts'
#     _description = 'Spending Accounts'
#
#     name = fields.Char(translate=True, required=True)
#     amount = fields.Float(required=True, default=0)
#     withdrew = fields.Float(default=0)
#     subtotal = fields.Float(default=False)
#     date_finish = fields.Date()
#     note = fields.Char()
#     user_id = fields.Many2one('res.users')


class Accounts(models.Model):
    _name = 'spending.accounts'
    _description = 'Spending Accounts'

    name = fields.Char(translate=True, required=True)
    amount = fields.Float(required=True, default=0)
    is_save = fields.Boolean(default=False, help="This account is use for saving. "
                                                 "You can use regular bank account as savings account.")
    transaction_in = fields.One2many()
    transaction_out = fields.One2many()
    note = fields.Char()
    user_id = fields.Many2one('res.users')


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


# class UseAccounts(models.Model):
#     _name = 'spending.accounts.use'
#     _inherit = 'spending.accounts'
