# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/almacenamiento/urls.py
Julian Perez
Ultima modificacion: Marzo 31 de 2009, 09:26
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

from django.conf.urls.defaults import *

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
""" Control del enrutamiento general del modulo de gestion de usuarios """

# Utilizando las vistas propias del modulo de almacenamiento
urlpatterns = patterns('savia.modulos.almacenamiento.views',

	# Ruta para visualizar el espacio de un usuario
	url(r'^mostrarEspacio/$', 'mostrarEspacio', name='enlace_mostrarEspacio'),

	# Rutas para subir un archivo a un espacio, y mostrar el progreso
	url(r'^subirArchivo/$', 'subirArchivo', name='enlace_subirArchivo'),
	url(r'^subirArchivo/progreso/$', 'subirArchivo_progreso', name='enlace_subirArchivo_progreso'),

)

# -----------------------------------------------------------------------