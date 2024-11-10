# -*- coding: utf-8 -*-
{
    'name': "Videoclub",

    'summary': """
        Gestión de alquileres de películas de un videoclub.""",

    'description': """
        Este módulo gestiona los alquileres de películas que realizan los socios del videoclub.
    """,

    'author': "Selene",
    'website': "https://es.wikipedia.org/wiki/Videoclub",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Administration',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/videoclub_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/videoclub_alquiler_report.xml',
        'data/videoclub_data.xml',
    ],
    'assets': {
       # Aquí añades tus archivos de bootstrap (que previamente has descargado y guardado en la carpeta /videoclub/static/)
       'web.assets_frontend': [
           '/videoclub/static/css/bootstrap.min.css',
           '/videoclub/static/js/bootstrap.min.js',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
     # Indicamos que es una aplicación
    'application': True,
}
