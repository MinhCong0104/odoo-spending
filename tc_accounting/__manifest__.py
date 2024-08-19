# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Thinh Cuong Accounting',
    'description': """Allow users manage their spending""",
    'version': '1.0',
    'category': 'Accounting/Accounting',
    'sequence': -100,
    'depends': ['account'],
    'data': [
        "security/ir.model.access.csv",
        "views/account_areas_views.xml",
        "views/menus.xml",
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
