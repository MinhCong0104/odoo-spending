# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _
from odoo.addons.spending.models.spending_transactions import TYPES_OF_TRANSACTION

_logger = logging.getLogger(__name__)


class Categories(models.Model):
    _name = 'spending.categories'
    _description = 'Spending Categories'

    name = fields.Char(translate=True, required=True)
    code = fields.Char(required=True)
    type = fields.Selection(TYPES_OF_TRANSACTION, required=True)
    note = fields.Char()
    report = fields.Boolean(string="Include on Report", default=True)
    user_id = fields.Many2one('res.users')

    _sql_constraints = [
        ('code_uniq', 'unique (code)', "This code already exists!"),
    ]
