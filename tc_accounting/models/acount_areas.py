# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class Limit(models.Model):
    _name = 'account.areas'
    _description = 'Account Areas'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    company_id = fields.Many2one('res.company', required=True)
    note = fields.Char()

    @api.constrains('name', 'code')
    def _check_name_code(self):
        # a = self.search_read([], fields=['name', 'code'])
        existing_names = []
        existing_codes = []
        for rec in self:
            if rec.name in existing_names:
                raise ValidationError(_('You are not allowed to request a time off on a Mandatory Day.'))
            if rec.code in existing_codes:
                raise ValidationError(_('You are not allowed to request a time off on a Mandatory Day.'))
