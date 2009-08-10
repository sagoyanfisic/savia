# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/usuarios/urls.py
Julian Perez
Ultima modificacion: Marzo 03 de 2009, 10:06
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

from django.contrib import admin
from django.conf.urls.defaults import *

# Habilitar el sitio de administracion proporcionado por Django
admin.autodiscover()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Control del enrutamiento general del modulo de gestion de usuarios """

# Utilizando las vistas propias del modulo de gestion de usaurios
urlpatterns = patterns('savia.modulos.usuarios.views',
	
	# Ruta para cambiar el tema actual
	url(r'^cambiartema/$', 'cambiarTema', name='enlace_cambiarTema'),		

	# Ruta para entrar al sitio de administracion
	url(r'^admin/(.*)', admin.site.root, name='enlace_sitioAdministracion'),

	# Ruta para terminar la sesion
	url(r'^terminarsesion/$', 'terminarSesion', name='enlace_terminarSesion'),
	
	# Rutas para la creacion de un nuevo usuario
	url(r'^dejalafluir/$', 'crearCuentaUsuario', name='enlace_crearCuentaUsuario'),
	url(r'^dejalafluir/consultarusuario/$', 'crearCuentaUsuario_consultar', name='enlace_crearCuentaUsuario_consultar'),
	url(r'^dejalafluir/activar/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'crearCuentaUsuario_activar', name='enlace_crearCuentaUsuario_activar'),

	# Rutas para la gestion del perfil de usuario
	url(r'^perfil/$', 'mostrarPerfil_principal', name='enlace_mostrarPerfil_principal'),
	url(r'^perfil/publico/(?P<nombreUsuarioAsociado>.+)/$', 'mostrarPerfil_publico', name='enlace_mostrarPerfil_publico'),
	url(r'^perfil/editar/informacion/$', 'editarPerfil_informacion', name='enlace_editarPerfil_informacion'),
   url(r'^perfil/editar/avatar/$', 'editarPerfil_avatar', name='enlace_editarPerfil_avatar'),
	url(r'^perfil/editar/avatar/recortarimagen/$', 'editarPerfil_avatar_recortarImagen', name='enlace_editarPerfil_avatar_recortarImagen'),
	url(r'^perfil/editar/avatar/eliminar/$', 'editarPerfil_avatar_eliminar', name='enlace_editarPerfil_avatar_eliminar'),
	url(r'^perfil/editar/ubicacion/$', 'editarPerfil_ubicacion', name='enlace_editarPerfil_ubicacion'),
	url(r'^perfil/editar/ubicacion/obtenerciudad/$', 'editarPerfil_ubicacion_obtenerCiudad', name='enlace_editarPerfil_ubicacion_obtenerCiudad'),

	# Rutas para la gestion de la contraseña
	url(r'^modificarcontrasena/$', 'modificarContrasena', name='enlace_modificarContrasena'),
	url(r'^recuperarcontrasena/$', 'recuperarContrasena', name='enlace_recuperarContrasena'),
	url(r'^recuperarcontrasena/confirmar/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'recuperarContrasena_confirmar', name='enlace_recuperarContrasena_confirmar'),
	
	# Rutas para eliminar la cuenta de usuario
  url(r'^eliminar/$', 'eliminarCuentaUsuario', name='enlace_eliminarCuentaUsuario'),
	
	#url(r'^flamas/$', 'iniciarFlamas', name='iniciarFlamas'),
	
)

# ----------------------------------------------------------------------