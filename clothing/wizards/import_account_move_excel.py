import logging

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


_logger = logging.getLogger(__name__)


# class TransientModel(models.TransientModel):
#     _name = "transient.model"
