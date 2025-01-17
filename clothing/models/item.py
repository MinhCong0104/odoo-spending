import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class Clothing(models.Model):
    _name = 'clothing.item'

    name = fields.Char('Tên', required=True)
    image = fields.Image('Hình ảnh')
    category_id = fields.Many2one('Loại')
    location_id = fields.Many2one('Vị trí')
    desc = fields.Text('Mô tả')
    size = fields.Char('Size')
    price = fields.Float('Giá')

    def action_move(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Wizard',
            'res_model': 'my.wizard',
            'view_mode': 'form',
            'target': 'new',  # 'new' để mở wizard trong modal popup
        }


class Category(models.Model):
    _name = 'clothing.category'

    name = fields.Char('Tên', required=True)
    code = fields.Char('Mã')


class Location(models.Model):
    _name = 'clothing.location'

    name = fields.Char('Tên', required=True)
    code = fields.Char('code')
