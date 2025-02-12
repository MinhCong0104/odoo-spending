# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError


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

    name = fields.Char('Name')
    date_from = fields.Date('Date from', default=_get_first_day_of_current_month())
    date_to = fields.Date('Date to', default=_get_last_day_of_current_month())
    note = fields.Text()
    line_ids = fields.One2many("spending.limit.line", "limit_id", copy=True)
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        default['date_from'] = self.date_from + relativedelta(months=1)
        default['date_to'] = self.date_to + relativedelta(months=1)
        return super(Limit, self).copy(default)

    @api.constrains('date_from', 'date_to')
    def _verify_date(self):
        for rec in self:
            if rec.date_to < rec.date_from:
                raise ValidationError(_("Date to can not before date from."))
            other_recs = self.sudo().search([
                ('id', '!=', rec.id), ('user_id', '=', rec.user_id.id), '|', '|',
                '&', ('date_from', '>=', rec.date_from), ('date_from', '<=', rec.date_to),
                '&', ('date_to', '>=', rec.date_from), ('date_to', '<=', rec.date_to),
                '&', ('date_from', '<=', rec.date_from), ('date_to', '>=', rec.date_to),
            ])
            if len(other_recs) > 0:
                raise ValidationError(_(f"Have another limit for this period: {rec.date_from} - {rec.date_to}"))


class LimitLine(models.Model):
    _name = 'spending.limit.line'
    _description = 'Spending Limit Line'

    limit_id = fields.Many2one("spending.limit", ondelete='cascade')
    date_from = fields.Date(related='limit_id.date_from')
    date_to = fields.Date(related='limit_id.date_to')
    category_id = fields.Many2one('spending.categories', 'Category', required=True)
    amount = fields.Monetary(required=True, default=0, currency_field='currency_id')
    remain = fields.Monetary(compute='_compute_remain', currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', default=lambda self: self.env.company.currency_id)
    note = fields.Char()
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)

    def _compute_remain(self):
        query = f"""
            SELECT COALESCE(SUM(amount), 0) AS amount
            FROM spending_transactions
            WHERE category_id = %(category_id)s
                AND type = 'spend'
                AND date BETWEEN %(date_from)s AND %(date_to)s
        """

        for rec in self:
            self.env.cr.execute(query, {'category_id': rec.category_id.id, 'date_from': rec.date_from, 'date_to': rec.date_to})
            spend = self.env.cr.dictfetchone()['amount']
            rec.remain = rec.amount - spend
