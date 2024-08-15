# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _


TYPES_OF_TRANSACTION = [('spend', 'Spend'), ('income', 'Income'), ('save', 'Save')]


_logger = logging.getLogger(__name__)


class Transactions(models.Model):
    _name = 'spending.transactions'
    _description = 'Spending Transactions'

    @api.model
    def default_get(self, fields):
        result = super(Transactions, self).default_get(fields)
        if 'recipient_ids' in fields and result.get('mail_message_id'):
            mail_message_id = self.env['mail.message'].browse(result['mail_message_id'])
            result['recipient_ids'] = [(0, 0, {
                'notification_id': notif.id,
                'resend': True,
                'failure_type': notif.failure_type,
                'partner_name': notif.res_partner_id.display_name or mail_message_id.record_name,
                'sms_number': notif.sms_number,
            }) for notif in mail_message_id.notification_ids if notif.notification_type == 'sms' and notif.notification_status in ('exception', 'bounce')]
        return result

    date = fields.Date(default=fields.Date.today(), required=True)
    amount = fields.Monetary(required=True, currency_field='currency_id')
    currency_id = fields.Many2one("res.currency", string='Currency', required=True)
    type = fields.Selection(TYPES_OF_TRANSACTION, required=True, default='spend', compute='_compute_type', store=True)
    purpose = fields.Selection([('transaction', 'Transaction'), ('save', 'Save'), ('invest', 'Invest')])
    category_id = fields.Many2one('spending.categories')
    is_save = fields.Boolean()
    from_account = fields.Many2one('spending.accounts')
    to_account = fields.Many2one('spending.accounts')
    note = fields.Char()
    user_id = fields.Many2one('res.users', readonly=True)

    @api.depends("category_id")
    def _compute_type(self):
        for rec in self:
            if rec.category_id:
                rec.type = rec.category_id.type
