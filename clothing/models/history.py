import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Clothing(models.Model):
    _name = 'clothing.history'

    time = fields.Datetime('Thời gian', default='')
    item_id = fields.Many2one('clothing.item', 'Trang phục')
    old_location_id = fields.Many2one('clothing.location', 'Vị trí cũ')
    current_location_id = fields.Many2one('clothing.location', 'Vị trí hiện tại')
    note = fields.Char('Ghi chú')
