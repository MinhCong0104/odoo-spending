# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _


TYPES_OF_TRANSACTION = [('spend', 'Spend'), ('income', 'Income'), ('save', 'Save'), ('internal', 'Internal')]


_logger = logging.getLogger(__name__)


class Transactions(models.Model):
    _name = 'spending.transactions'
    _description = 'Spending Transactions'

    date = fields.Date(default=fields.Date.today(), required=True)
    amount = fields.Monetary(required=True, currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', required=True)
    type = fields.Selection(TYPES_OF_TRANSACTION,  default='spend',
                            compute='_compute_type', store=True, required=True, readonly=False)
    purpose = fields.Selection([('transaction', 'Transaction'), ('save', 'Save'), ('invest', 'Invest')])
    category_id = fields.Many2one('spending.categories')
    is_save = fields.Boolean()
    from_account = fields.Many2one('spending.accounts')
    to_account = fields.Many2one('spending.accounts')
    note = fields.Text()
    user_id = fields.Many2one('res.users', readonly=True)

    # Tính toán trường purpose (mục đích sử dụng) dựa trên đặc điểm của giao dịch
    # 1. chi tiêu: type = spend
    # 2. thu nhập: type = income
    # 3. chuyển tiền nội bộ: type = internal, cả tài khoản gửi và nhận đều là tài khoản chi tiêu
    # 4. tiết kiệm: type = internal, tài khoản nhận là save
    # 5. đầu tư: type = internal, tài khoản nhận là invest
