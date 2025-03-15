# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class Withdraw(models.TransientModel):
    _name = 'spending.withdraw'

    from_account = fields.Many2one('spending.accounts')
    to_account = fields.Many2one('spending.accounts')

    def action_withdraw(self):
        self.ensure_one()
        # rút tiền internal
        # ghi lãi income
