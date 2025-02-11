# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Transactions(models.Model):
    _name = 'spending.transactions'
    _description = 'Spending Transactions'
    _order = 'date desc, id desc'

    date = fields.Date(default=fields.Date.context_today, required=True)
    amount = fields.Monetary(required=True, currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', default=lambda self: self.env.company.currency_id)
    type = fields.Selection([('spend', 'Spend'), ('income', 'Income'), ('internal', 'Internal')], default='spend', required=True)
    category_id = fields.Many2one('spending.categories', 'Category')
    from_account = fields.Many2one('spending.accounts')
    to_account = fields.Many2one('spending.accounts')
    note = fields.Text()
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
