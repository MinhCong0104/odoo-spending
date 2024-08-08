# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Personal Spending',
    'description': """Allow users manage their spending""",
    'version': '1.0',
    'category': 'Financial',
    'sequence': -100,
    'depends': [],
    'data': [
        "security/ir.model.access.csv",
        "security/spending_security.xml",

        "views/spending_categories_views.xml",
        "views/spending_accounts_views.xml",
        "views/spending_limit_views.xml",
        "views/spending_transactions_views.xml",

        "views/spending_menus.xml",
    ],
    # 'bootstrap': True,
    # 'assets': {
    #     'web.assets_frontend': [
    #         'auth_signup/static/**/*',
    #     ],
    # },
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
