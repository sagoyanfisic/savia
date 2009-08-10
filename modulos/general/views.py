# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/general/views.py
Julian Perez
Ultima modificacion: Agosto 01 de 2009, 09:51
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.sites.models import RequestSite
from savia.modulos.usuarios.models import Perfil
from savia.modulos.general.forms import ContactoFormulario
from savia.modulos.utilidades.utils import *

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarInicio: muestra la pagina de inicio adecuada
"""

def mostrarInicio(peticion):
	usuarioActual = peticion.user
	# Crea el archivo de variables globales de Javascript, indispensable para la buena ejecucion del sitio
	crearArchivoVariablesEntornoJS('base_variables')
	# Si trata de acceder un usuario en sesion actualmente o ya registrado
	if not usuarioActual.is_anonymous():
		# Si el usuario tienen permisos de administrador
		if usuarioActual.is_staff == True:
			# Redireccionar al sitio de administracion
			return HttpResponseRedirect(settings.URL_PREFIJO+ 'usuarios/admin/')
		else:
			# Mostrar la plantilla de inicio de los usuarios que ya iniciaron sesion
			return render_to_response('general/mostrarInicio_inicio.html', context_instance=RequestContext(peticion))
	# Mostrar y manipular el formulario de inicio de sesion
	else:
		diccionario = {  }
		if peticion.method == 'POST':
			# Capturando los datos de POST
			nombreUsuario = peticion.POST['username']
			contrasena = peticion.POST['password']
			# Autenticar al usuario comprobando el nombre de usuario y la contraseña
			usuarioActual = auth.authenticate(username=nombreUsuario, password=contrasena)
			# Si el usuario es activo y valido en el sistema
			if usuarioActual is not None:
				# Si la cuenta actual esta activa
				if usuarioActual.is_active:
					fechaUltimaVisita = usuarioActual.last_login
					# Iniciar la sesion
					auth.login(peticion, usuarioActual)
					if usuarioActual.is_staff == True:
						return HttpResponseRedirect(settings.URL_PREFIJO+ 'usuarios/admin/')
					else:						
						perfilActual, fueCreado = Perfil.objects.get_or_create(user=usuarioActual)
						perfilActual.numeroVisitas += 1
						perfilActual.save()
						return render_to_response('general/mostrarInicio_inicio.html', { 'fechaUltimaVisita' : fechaUltimaVisita, }, context_instance=RequestContext(peticion))
				else:
					iniciarSesion_error = 'La cuenta de usuario <i>' +nombreUsuario+ '</i> est&aacute; actualmente inactiva.'
			else:
				iniciarSesion_error = 'La combinaci&oacute;n digitada de <i>Nombre de usuario</i> y <i>Contrase&ntilde;a</i> es incorrecta.'
			diccionario = { 'iniciarSesion_error' : 'Espera un momento...<br/>Hay problemas.<br/>' +iniciarSesion_error, }
		return render_to_response('general/mostrarInicio_index.html', diccionario, context_instance=RequestContext(peticion))		

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarError403: muestra la plantilla de error 403
"""
def mostrarError403(peticion):
	return render_to_response('403.html', context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarAcercade: muestra la plantilla tipo 'acerca de' o de agradecimientos
"""

def mostrarAcercade(peticion):
	return render_to_response('general/mostrarAcercade.html', context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarAyuda: muestra la plantilla de ayuda tipo 'FAQ'
"""

def mostrarAyuda(peticion):
	return render_to_response('general/mostrarAyuda.html', context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarContacto: muestra y manipula el formulario de contacto con el administrador del sistema
"""

def mostrarContacto(peticion):
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = ContactoFormulario(peticion.POST)			
		# Si es formulario es correcto
		if formulario.is_valid():
			# Envia el mensaje al administrador, bien sea por correo electronico o por el sistema interno
			usuarioActual = peticion.user	
			formulario.save(usuarioActual, esConexionSegura=peticion.is_secure(), sobreescribirDominio=RequestSite(peticion).domain)
			return render_to_response('general/mostrarContacto.html', context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		formulario = ContactoFormulario()
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, }
	return render_to_response('general/mostrarContacto.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------