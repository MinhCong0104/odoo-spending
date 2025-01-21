import logging
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


class Action(models.TransientModel):
    _name = "closing.action"

    item_ids = fields.Many2many('closing.item', 'Trang phục')
    location_id = fields.Many2one('closing.location', 'Vị trí')
    note = fields.Char('Ghi chú')

    def action_confirm(self):
        self.ensure_one()
        self.env['clothing.history'].create({
            'time': datetime.now(),
            'item_id': item.id,
            'old_location_id': item.location_id.id,
            'current_location_id': self.location_id.id,
            'note': self.note,
        } for item in self.item_ids)
        self.item_ids.sudo.write({'location_id': self.location_id.id})
        return {'type': 'ir.actions.act_window_close'}
