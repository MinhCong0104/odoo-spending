# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import calendar
from datetime import datetime

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


def _get_first_day_of_current_month():
    return datetime.today().replace(day=1)


def _get_last_day_of_current_month():
    today = datetime.today()
    last_day = calendar.monthrange(today.year, today.month)[1]
    return today.replace(day=last_day).date()


class Limit(models.Model):
    _name = 'spending.limit'
    _description = 'Spending Limit'

    name = fields.Char('Tên')
    date_from = fields.Date('Date from', default=_get_first_day_of_current_month())
    date_to = fields.Date('Date to', default=_get_last_day_of_current_month())
    note = fields.Text()
    line_ids = fields.One2many("spending.limit.line", "limit_id")
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)


class LimitLine(models.Model):
    _name = 'spending.limit.line'
    _description = 'Spending Limit Line'

    limit_id = fields.Many2one("spending.limit", ondelete='cascade')
    date_from = fields.Date(related='limit_id.date_from')
    date_to = fields.Date(related='limit_id.date_to')
    category_id = fields.Many2one('spending.categories', 'Category')
    amount = fields.Monetary(required=True, default=0, currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', default=lambda self: self.env.company.currency_id)
    note = fields.Char()
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
