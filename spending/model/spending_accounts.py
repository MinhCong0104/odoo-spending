# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Accounts(models.Model):
    _name = 'spending.accounts'
    _description = 'Spending Accounts'

    name = fields.Char(translate=True, required=True)
    amount = fields.Float(required=True, default=0)
    withdrew = fields.Float(default=0)
    subtotal = fields.Float(default=False)
    date_finish = fields.Date()
    note = fields.Char()
    user_id = fields.Many2one('res.users')
