from odoo import http
from odoo.http import request

#
# class EmployeeDetailBook(http.Controller):
#
#     @http.route('/tc_accounting/update_dimension_value', type="json", auth="user")
#     def update_dimension_value(self, *kw):
#         id = request.params.get('id')
#         value_ids = request.params.get('value_ids')
#
#         wz = request.env['update.dimension.move.line.wz'].sudo().browse(id)
#         wz.update({
#             'value_ids': [(6,0,value_ids)]
#         })
#         return True