# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Categories(models.Model):
    _name = 'spending.categories'
    _description = 'Spending Categories'

    name = fields.Char(translate=True, required=True)
    type = fields.Selection([('spend', 'Spend'), ('income', 'Income'), ('internal', 'Internal')], default='spend', required=True)
    report = fields.Boolean(string="Include on Report", default=True)
    note = fields.Char()
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
