# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/general/urls.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 10:06
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

from django.conf.urls.defaults import *
from django.conf import settings

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
""" Control del enrutamiento general de savia """

urlpatterns = patterns('',

	# Ruta para los archivos estaticos
   url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),

	# Ruta de inicio
	url(r'^$', 'savia.modulos.general.views.mostrarInicio', name='enlace_mostrarInicio'),	
	
	# Ruta para mostrar la plantilla de error 403 (acceso restringido)
	url(r'^error403/$', 'savia.modulos.general.views.mostrarError403', name='enlace_mostrarError403'),

	# Ruta para mostrar la plantilla de agradecimientos
	url(r'^acercade/$', 'savia.modulos.general.views.mostrarAcercade', name='enlace_mostrarAcercade'),	
	
	# Rutas para la ayuda y el contatco con el administrador del sistema
	url(r'^ayuda/$', 'savia.modulos.general.views.mostrarAyuda', name='enlace_mostrarAyuda'),
	url(r'^contacto/$', 'savia.modulos.general.views.mostrarContacto', name='enlace_mostrarContacto'),		
	
	# Ruta para el modulos de gestion de usuarios: utiliza savia.modulos.usuarios.urls
	url(r'^usuarios/', include('savia.modulos.usuarios.urls')),	
	
	# Ruta para el modulos de gestion de relaciones: utiliza savia.modulos.relaciones.urls
	url(r'^relaciones/', include('savia.modulos.relaciones.urls')),	

	# Ruta para el modulo de almacenamiento: utiliza savia.modulos.almacenamiento.urls
   url(r'^almacenamiento/', include('savia.modulos.almacenamiento.urls')),

)

# -----------------------------------------------------------------------