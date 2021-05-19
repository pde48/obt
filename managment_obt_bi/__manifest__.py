# -*- coding: utf-8 -*-
{
    'name': "Obt Managment",

    'summary': """
        Mamagment Obt""",

    'description': """
        Mamagment Obt
    """,
    'author': "Cabatel",
    'website': "http://www.obt.com",
    'category': 'Purchase',
    'version': '0.1',
    'depends': ['base_setup','utm','mail','contacts','portal',],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
}
