# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/utildiades/contexto.py
Julian Perez
Ultima modificacion: Agosto 01 de 2009, 21:35
"""
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
""" Importaciones """

from django.conf import settings
from savia.modulos.relaciones.models import Mensaje, Amistad

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
""" Funciones auxiliares """

def calcularNumeroMensajesNuevos(usuarioActual):
	try:
		numeroMensajesNuevos = Mensaje.objects.filter(usuarioDestino=usuarioActual, esNuevo=True, disponibleDestino=True).count()
	except:
		numeroMensajesNuevos = None
	return numeroMensajesNuevos
	
def calcularNumeroSolicitudesAmistadNuevas(usuarioActual):
	try:
		numeroMensajesNuevos = Amistad.objects.filter(usuarioConfirmante=usuarioActual, esSolicitudAprobada=False).count()
	except:
		numeroMensajesNuevos = None
	return numeroMensajesNuevos	

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
""" Funcion que inicializa el contexto personalizado """

def inicializarContexto(peticion):
	diccionario =  {
		'nombreAplicacion' : settings.NOMBRE_APLICACION,
		'versionActual' : settings.VERSION_APLICACION,
		'usuarioActual' : peticion.user,
		'usuarioAdministrador' : settings.NOMBRE_USUARIO_ADMIN,
		'usuarioAnonimo' : settings.NOMBRE_USUARIO_ANONIMO,
		'peticionActual' : peticion,
		'rutaActual' : peticion.path,
		'errores_errorFormulario' : 'Espera un momento...<br/>El formulario que enviaste contiene errores.<br/>Por favor, verifica los campos se&ntilde;alados',
		'contadorMensajesNuevos' : calcularNumeroMensajesNuevos(peticion.user),
		'contadorSolicitudesAmistadNuevas' : calcularNumeroSolicitudesAmistadNuevas(peticion.user),
	}
	return diccionario		

# -----------------------------------------------------------------------