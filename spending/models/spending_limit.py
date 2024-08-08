# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _


_logger = logging.getLogger(__name__)


class Limit(models.Model):
    _name = 'spending.limit'
    _description = 'Spending Limit'

    amount = fields.Monetary(required=True, default=0, currency_field='currency_id')
    remain = fields.Monetary(readonly=True, currency_field='currency_id', compute='_compute_remain')
    currency_id = fields.Many2one("res.currency", string='Currency', required=True)
    date_from = fields.Date()
    date_to = fields.Date()
    note = fields.Char()
    category_id = fields.Many2one('spending.categories')
    user_id = fields.Many2one('res.users')

    def _compute_remain(self):
        for rec in self:
            self.env.cr.execute(f"""
                SELECT sum(amount) FROM spending_transactions 
                WHERE category_id = {rec.category_id.id}
                      AND date <= %s 
                      AND date >= %s
            """, [rec.date_to, rec.date_from])
            res = self.env.cr.fetchall()
            amount_spent = 0 if not res[0][0] else res[0][0]
            rec.remain = rec.amount - amount_spent

    def _compute_transactions(self):
        pass
