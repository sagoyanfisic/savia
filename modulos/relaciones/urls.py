# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/relaciones/urls.py
Julian Perez
Ultima modificacion: Agosto 01 de 2009, 10:06
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

from django.contrib import admin
from django.conf.urls.defaults import *

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Control del enrutamiento general del modulo de relaciones """

# Utilizando las vistas propias del modulo de relaciones
urlpatterns = patterns('savia.modulos.relaciones.views',
	
	# Ruta para enviar un mensaje
	url(r'^mensajes/enviar/$', 'enviarMensaje', name='enlace_enviarMensaje'),	

	# Ruta para ver los mensajes recibidos
	url(r'^mensajes/recibidos/$', 'mostrarMensajes_recibidos', name='enlace_mostrarMensajes_recibidos'),
	
	# Ruta para responder un mensaje a su destino especifico
	url(r'^mensajes/responder/(?P<idMensaje>[0-9]+)/$', 'responderMensaje', name='enlace_responderMensaje'),		
	url(r'^mensajes/respondercorreo/(?P<idMensaje>[0-9]+)/$', 'enviarCorreo', name='enlace_enviarCorreo'),
	
	# Ruta para ver los mensajes enviados
	url(r'^mensajes/enviados/$', 'mostrarMensajes_enviados', name='enlace_mostrarMensajes_enviados'),			
	
	# Rutas para la lectura de un mensaje especifico
	url(r'^mensajes/recibidos/leer/(?P<idMensaje>[0-9]+)/$', 'leerMensaje_recibido', name='enlace_leerMensaje_recibido'),		
	url(r'^mensajes/enviados/leer/(?P<idMensaje>[0-9]+)/$', 'leerMensaje_enviado', name='enlace_leerMensaje_enviado'),	
	
	# Rutas para la gestion de un mensaje especifico
	url(r'^mensajes/modificarestado/(?P<idMensaje>[0-9]+)/$', 'editarMensaje_modificarEstado', name='enlace_editarMensaje_modificarEstado'),
	url(r'^mensajes/eliminar/(?P<idMensaje>[0-9]+)/$', 'eliminarMensaje', name='enlace_eliminarMensaje'),
	
	# Ruta para buscar usuarios
	url(r'^amistades/busqueda/$', 'busquedaUsuarios', name='enlace_busquedaUsuarios'),		
	
	# Ruta para ver el perfil extendido de un usuario
	url(r'^amistades/perfil/(?P<nombreUsuarioAsociado>.+)/$', 'mostrarPerfilExtendido', name='enlace_mostrarPerfilExtendido'),
	
	# Ruta para enviar una solicitud de amistad a un usuario especifico
	url(r'^amistades/solicitar/(?P<nombreUsuarioSolicitado>.+)/$', 'enviarSolicitudAmistad', name='enlace_enviarSolicitudAmistad'),	
	
	# Ruta para ver la lista de solicitudes de amistad recibidas
	url(r'^amistades/solicitudes/$', 'mostrarSolicitudesAmistad', name='enlace_mostrarSolicitudesAmistad'),		
	
	# Ruta para la gestion de una solicitud de amistad especifica
	url(r'^amistades/solicitudes/aprobar/(?P<idSolicitud>[0-9]+)/$', 'editarSolicitudAmistad_aprobar', name='enlace_editarSolicitudAmistad_aprobar'),
	url(r'^amistades/solicitudes/rechazar/(?P<idSolicitud>[0-9]+)/$', 'editarSolicitudAmistad_rechazar', name='enlace_editarSolicitudAmistad_rechazar'),	
	
	# Ruta para ver la lista de amigos
	url(r'^amistades/listaamigos/$', 'mostrarListaAmigos', name='enlace_mostrarListaAmigos'),		
	
	# Rutas para la gestion de un amigo especifico
	url(r'^amistades/modificarestado/(?P<idAmistad>[0-9]+)/$', 'editarAmistad_modificarEstado', name='enlace_editarAmistad_modificarEstado'),
	url(r'^amistades/eliminar/(?P<idAmistad>[0-9]+)/$', 'eliminarAmistad', name='enlace_eliminarAmistad'),	
	
)

# ----------------------------------------------------------------------