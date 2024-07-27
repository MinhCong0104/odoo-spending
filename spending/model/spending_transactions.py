# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _
TYPE = [('spend', 'Spend'), ('income', 'Income'), ('save', 'Save')]

_logger = logging.getLogger(__name__)


class Transactions(models.Model):
    _name = 'spending.transactions'
    _description = 'Spending Transactions'

    date = fields.Date(default=fields.Date.today(), required=True)
    amount = fields.Float(required=True)
    type = fields.Selection(TYPE, required=True)
    purpose = fields.Selection([('transaction', 'Transaction'), ('save', 'Save'), ('invest', 'Invest')])
    category_id = fields.Many2one('spending.categories')
    from_account = fields.Many2one('spending.accounts')
    to_account = fields.Many2one('spending.accounts')
    note = fields.Char()
    user_id = fields.Many2one('res.users', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('from_account'):
                # trừ tiền
                pass
            if vals.get('to_account'):
                # cộng tiền
                pass
        return super().create(vals_list)
