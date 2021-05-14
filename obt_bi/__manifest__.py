# -*- coding: utf-8 -*-
{
    'name': "OBT BI",

    'summary': """
        Modulo que procesa informacion en los procesos de cria y engorde Ganado""",

    'description': """
    Modulo que procesa informacion en los procesos de cria y engorde Ganado    """,

    'author': "Cabatel to OBT",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchases',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','contacts','account'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/view_obt_bi.xml',
        #'views/templates.xml',
    ],
    'demo': [
    ],
}