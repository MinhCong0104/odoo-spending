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
    remain = fields.Float(readonly=True, compute='_compute_remain')
    date_from = fields.Date()
    date_to = fields.Date()
    note = fields.Char()
    category_id = fields.Many2one('spending.categories')
    user_id = fields.Many2one('res.users')

    def _compute_remain(self):
        # Method này chưa xong
        # Logic: query tất cả các transactions có category này trong khoảng thời gian này, tính tổng amount rồi trừ đi
        for rec in self:
            self.env.cr.execute(f"""
                SELECT sum(amount) FROM spending_transactions 
                WHERE category_id = {rec.category_id.id}
            """)
            res = self.env.cr.fetchall()
            rec.remain = rec.amount - res[0][0]
