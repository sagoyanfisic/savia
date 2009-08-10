# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/configuracion/servidor.wsgi
Julian Perez
Ultima modificacion: Abril 24 de 2009, 22:14
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import os
import os.path
import sys

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Incluyendo el directorio de savia para que sea cargado junto a Python cuando inicia Apache """

savia_configuracion = os.path.dirname(__file__)
savia = os.path.dirname(savia_configuracion)
espacio = os.path.dirname(savia)
sys.path.append(espacio)
sys.path.append(os.path.join(espacio, '../'))

os.environ['DJANGO_SETTINGS_MODULE'] = 'savia.settings'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Creacion del objeto WSGI para el control de savia por medio de Apache """

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()

# ----------------------------------------------------------------------