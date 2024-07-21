# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Limit(models.Model):
    _name = 'spending.limit'
    _description = 'Spending Limit'

    name = fields.Char(translate=True, required=True)
    amount = fields.Float(required=True, default=0)
    remain = fields.Float(readonly=True)
    date_from = fields.Date()
    date_to = fields.Date()
    note = fields.Char()
    category_id = fields.Char()
    user_id = fields.Many2one('res.users')
