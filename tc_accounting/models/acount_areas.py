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

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Name already exists!"),
        ('code_uniq', 'unique (code)', "Code already exists!"),
    ]
