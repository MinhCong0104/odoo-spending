# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Transactions(models.Model):
    _name = 'spending.transactions'
    _description = 'Spending Transactions'

    name = fields.Char(translate=True, required=True)
    amount = fields.Float(required=True)
    category_id = fields.Many2one('spending.categories')
    from_account = fields.Many2one('spending.accounts')
    note = fields.Char()
    user_id = fields.Many2one('res.users', readonly=True)
