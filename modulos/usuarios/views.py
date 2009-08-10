# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/usuarios/views.py
Julian Perez
Ultima modificacion: Abril 26 de 2009, 09:51
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import re
import urllib
import Image
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.utils import simplejson
from django.utils.http import base36_to_int
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from xml.dom import minidom
from django.template import RequestContext
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.sites.models import RequestSite
from savia.modulos.usuarios.models import Perfil, Avatar
from savia.modulos.relaciones.models import Amistad, sonAmigos, existeSolicitudAmistad, crearReporteActividadReciente
from savia.modulos.usuarios.forms import RegistroFormulario, EliminarCuentaUsuarioFormulario
from savia.modulos.usuarios.forms import PerfilFormulario, AvatarFormulario, RecortarImagenFormulario, UbicacionFormulario
from savia.modulos.usuarios.forms import EstablecerContrasenaFormulario, ModificarContrasenaFormulario, RecuperarContrasenaFormulario
from savia.modulos.utilidades.utils import crearCaptcha, verificarCaptcha, eliminarCaptcha, crearImagenDireccionCorreo, calcularEdad, eliminarImagenesAsociadas

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista cambiarTema: registra el cambio del tema actual
"""

@login_required
def cambiarTema(peticion):
	if peticion.is_ajax():
		usuarioActual = peticion.user
		try:
			temaElegido = peticion.POST['temaElegido']
			perfilActual = Perfil.objects.get(user=usuarioActual)
			perfilActual.temaPreferido = temaElegido
			perfilActual.save()
			print perfilActual.user
			return HttpResponse('respuestaServidor_exito')
		except:
			return HttpResponse('respuestaServidor_error')
	else:
		raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista terminarSesion: termina la sesion del usuario actual
"""

def terminarSesion(peticion):
	usuarioActual = peticion.user
	# Si trata de acceder un usuario sin sesion actualmente
	if usuarioActual.is_anonymous():
		return HttpResponseRedirect(reverse('enlace_mostrarInicio'))
	else:
		# Cerrar la sesion actual
		auth.logout(peticion)
		# Redireccionar hacia la plantilla de despedida
		return HttpResponseRedirect(reverse('enlace_mostrarInicio'))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista crearCuentaUsuario: muestra y manipula el formulario de registro un nuevo usuario
"""

def crearCuentaUsuario(peticion):
	usuarioActual = peticion.user
	# Si trata de acceder un usuario en sesion actualmente
	if not usuarioActual.is_anonymous():
		return HttpResponseRedirect(reverse('enlace_mostrarInicio'))
	else:
		# Si hay alguna peticion (formulario con datos) se procesa el formulario
		if peticion.method == 'POST':
			formulario = RegistroFormulario(peticion.POST)
			codigoCaptchaGenerado = peticion.POST['captchaGenerado']
			codigoCaptchaDigitado = peticion.POST['captchaDigitado'].upper()
			# Verificar primero si el captcha es correcto
			if verificarCaptcha(codigoCaptchaGenerado,codigoCaptchaDigitado):
				errorCaptcha = False
				eliminarCaptcha(codigoCaptchaGenerado)
				# Si el formulario es correcto
				if formulario.is_valid():
					# Ingresando la cuenta de usuario
					nombreElegido = formulario.cleaned_data.get('nombreElegido')
					contrasena = formulario.cleaned_data.get('contrasena1')
					correo = formulario.cleaned_data.get('correo')
					usuarioNuevo = User.objects.create_user(username=nombreElegido, email=correo, password=contrasena)
					nombres = formulario.cleaned_data.get('nombres')
					apellidos = formulario.cleaned_data.get('apellidos')
					usuarioNuevo.first_name =	nombres
					usuarioNuevo.last_name = apellidos
					# La cuenta se crea pero no se activa
					usuarioNuevo.is_active = False
					usuarioNuevo.save()
					# Ingresando el perfil de usuario
					perfilNuevo = Perfil.objects.create(user=usuarioNuevo)
					perfilNuevo.save()
					# Ingresando la amistad exclusiva entre el administrador y cada usuario existente				
					usuarioAdministrador = User.objects.get(username=settings.NOMBRE_USUARIO_ADMIN)
					amistadNueva = Amistad.objects.create(usuarioSolicitante=usuarioNuevo, usuarioConfirmante=usuarioAdministrador, esSolicitudAprobada=True, modoAdministrador=True)
					amistadNueva.save()
					# Reportando la actividad reciente
					crearReporteActividadReciente(usuarioNuevo, u' es desde hoy uno m&aacute;s que deja fluir la sabia savia')
					# Enviar el mensaje de correo
					formulario.save(esConexionSegura=peticion.is_secure(), sobreescribirDominio=RequestSite(peticion).domain)		
					return render_to_response('usuarios/crearCuentaUsuario.html', context_instance=RequestContext(peticion))
				# Si el captcha es incorrecto
				else:
					errorCaptcha = False
			# Si el formulario contiene errores
			else:
				errorCaptcha = True
			errorOperacion = True
		# Si no hay alguna peticion se muestra el formulario
		else:
			formulario = RegistroFormulario()
			errorOperacion = False
			errorCaptcha = False
		captchaGenerado, rutaCaptcha = crearCaptcha()
		diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, 'captchaGenerado' : captchaGenerado, 'rutaCaptcha' : rutaCaptcha, 'errorCaptcha' : errorCaptcha }
		return render_to_response('usuarios/crearCuentaUsuario.html', diccionario, context_instance=RequestContext(peticion))	

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista crearUsuario_consultar: consulta si un nombre de usuario especifico esta disponible
"""

def crearCuentaUsuario_consultar(peticion):
	if peticion.is_ajax():
		nombreElegido = peticion.POST['nombreElegido']
		if User.objects.filter(username__iexact=nombreElegido).count() == 0:
			return HttpResponse('respuestaServidor_exito')
		else:
			return HttpResponse('respuestaServidor_error')
	else:
		raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista crearCuentaUsuario_activar: muestra y manipula el formulario de activacion de la cuenta de usuario
"""

def crearCuentaUsuario_activar(peticion, uidb36=None, token=None):
	usuarioActual = peticion.user
	# Si trata de acceder un usuario en sesion actualmente
	if not usuarioActual.is_anonymous():
		return HttpResponseRedirect(reverse('enlace_mostrarInicio'))
	else:
		assert uidb36 is not None and token is not None
		try:
			uid_int = base36_to_int(uidb36)
		except ValueError:
			raise Http404
		usuarioActual = get_object_or_404(User, id=uid_int)
		# Si el enlace es valido
		if default_token_generator.check_token(usuarioActual, token) and not usuarioActual.is_active:
			enlaceValido = True
			# Activando la cuenta de usuario
			usuarioActual.is_active = True
			usuarioActual.save()
		else:
			enlaceValido = False
		diccionario = { 'enlaceValido' : enlaceValido, }
		return render_to_response('usuarios/crearCuentaUsuario_activar.html', diccionario, context_instance=RequestContext(peticion))
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarPerfil_principal: muestra el perfil propio de un usuario
"""

@login_required
def mostrarPerfil_principal(peticion):
	usuarioActual = peticion.user
	perfilActual = Perfil.objects.get(user=usuarioActual)
	rutaImagenDireccionCorreo = crearImagenDireccionCorreo(peticion.user)
	diccionario = { 'perfilActual' : perfilActual, 'llaveGoogleMaps': settings.LLAVE_GOOGLEMAPS, 'rutaImagenDireccionCorreo' : rutaImagenDireccionCorreo, }
	return render_to_response('usuarios/mostrarPerfil_principal.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarPerfil_publico: muestra el perfil publico de un usuario
"""

def mostrarPerfil_publico(peticion, nombreUsuarioAsociado):
	if nombreUsuarioAsociado == settings.NOMBRE_USUARIO_ADMIN:
		return HttpResponseRedirect(reverse('enlace_mostrarAcercade'))
	else:
		perfilPublico = get_object_or_404(User, username=nombreUsuarioAsociado, is_staff=False).get_profile()
		diccionario = { 'perfilPublico' : perfilPublico, 'llaveGoogleMaps': settings.LLAVE_GOOGLEMAPS, 'edadUsuario': calcularEdad(perfilPublico.fechaNacimiento) }
		return render_to_response('usuarios/mostrarPerfil_publico.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarPerfil_informacion: muestra y manipula el formulario de modificacion de la informacion del perfil de un usuario
"""

@login_required
def editarPerfil_informacion(peticion):
	usuarioActual = peticion.user
	perfilActual = Perfil.objects.get(user=usuarioActual)
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = PerfilFormulario(peticion.POST, instance=perfilActual)
		# Si es formulario es correcto
		if formulario.is_valid():
			formulario.save()
			# Reportando la actividad reciente
			crearReporteActividadReciente(usuarioActual, u'edit&oacute; la informaci&oacute;n personal de su perfil')
			diccionario = { 'formulario' : formulario, 'exitoOperacion' : True, 'generoActual' : perfilActual.sexo, 'fechaNacimientoActual' : perfilActual.fechaNacimiento, }
			return render_to_response('usuarios/editarPerfil_informacion.html', diccionario, context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		formulario = PerfilFormulario(instance=perfilActual)
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, 'generoActual' : perfilActual.sexo, 'fechaNacimientoActual' : perfilActual.fechaNacimiento, }
	return render_to_response('usuarios/editarPerfil_informacion.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarPerfil_avatar: muestra y manipula el formulario para subir la imagen del avatar del usuario
"""

@login_required
def editarPerfil_avatar(peticion):
	usuarioActual = peticion.user
	perfilActual = Perfil.objects.get(user=usuarioActual)
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = AvatarFormulario(peticion.POST, peticion.FILES)
		# Si el formulario es correcto
		if formulario.is_valid():
			imagen = formulario.cleaned_data.get('imagen')
			avatarActual = Avatar(usuarioAsociado=usuarioActual, imagen=imagen, esValida=False)
			avatarActual.imagen.save('%s.jpg' % usuarioActual.username, imagen)
			imagenAvatar = Image.open(avatarActual.imagen.path)
			imagenAvatar.thumbnail((777, 777), Image.ANTIALIAS)
			imagenAvatar.convert('RGB').save(avatarActual.imagen.path, 'JPEG')
			avatarActual.save()
			return HttpResponseRedirect(reverse('enlace_editarPerfil_avatar_recortarImagen'))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		# Si la pagina anterior fue la de recortar la imagen
		try:
			if re.search(reverse('enlace_editarPerfil_avatar_recortarImagen'),peticion.META['HTTP_REFERER']):
				exitoOperacion = True
				# Reportando la actividad reciente
				crearReporteActividadReciente(usuarioActual, u'cambi&oacute; de avatar de usuario')				
			else:
				exitoOperacion = False
		except KeyError:
			exitoOperacion = False
		formulario = AvatarFormulario()
		errorOperacion = False
	# Obteniendo la ruta del avatar generico
	avatarGenerico = settings.URL_AVATAR_GENERICO
	diccionario = { 'formulario' : formulario, 'exitoOperacion' : exitoOperacion,  'errorOperacion' : errorOperacion, 'avatarGenerico' : avatarGenerico, }
	return render_to_response('usuarios/editarPerfil_avatar.html', diccionario, context_instance=RequestContext(peticion))
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarPerfil_avatar_recortarImagen: muestra el formulario de recorte de la imagen elegida como avatar de usuario
"""

@login_required
def editarPerfil_avatar_recortarImagen(peticion):
	usuarioActual = peticion.user
	avatarActual = get_object_or_404(Avatar, usuarioAsociado=usuarioActual, esValida=False)
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = RecortarImagenFormulario(peticion.POST)
		# Si es formulario es correcto
		if formulario.is_valid():
			# Obteniendo las coordenadas de la region seleccionada en la imagen
			arriba = formulario.cleaned_data.get('arriba')
			abajo = formulario.cleaned_data.get('abajo')
			izquierda = formulario.cleaned_data.get('izquierda')
			derecha = formulario.cleaned_data.get('derecha')
			imagenElegida = Image.open(avatarActual.imagen.path)
			area = [ izquierda, arriba, derecha, abajo ]
			# Extrayendo la region seleccionada de la imagen completa
			imagenElegida = imagenElegida.crop(area)
			if imagenElegida.mode not in ('L', 'RGB'):
				imagenElegida = imagenElegida.convert('RGB')
			# Validando la imagen y almacenandola
			imagenElegida.thumbnail((96, 96), Image.ANTIALIAS)
			imagenElegida.save(avatarActual.imagen.path)
			avatarActual.esValida = True
			avatarActual.save()
			return HttpResponseRedirect(reverse('enlace_editarPerfil_avatar'))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	else:
		formulario = RecortarImagenFormulario()
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, 'avatarActual' : avatarActual, }
	return render_to_response('usuarios/editarPerfil_avatar_recortarImagen.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarPerfil_avatar_eliminar: elimina el avatar actual del usuario
"""

@login_required
def editarPerfil_avatar_eliminar(peticion):
	if peticion.is_ajax():
		try:
			usuarioActual = peticion.user
			avatarActual = Avatar.objects.get(usuarioAsociado=usuarioActual, esValida=True)
			avatarActual.delete()
			eliminarImagenesAsociadas(usuarioActual.username)
			return HttpResponse('respuestaServidor_exito')
		except:
			return HttpResponse('respuestaServidor_error')
	else:
		raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarPerfil_ubicacion: muestra y manipula el formulario la ubicacion geografica del usuario
"""

@login_required
def editarPerfil_ubicacion(peticion):
	usuarioActual = peticion.user
	perfilActual = Perfil.objects.get(user=usuarioActual)
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = UbicacionFormulario(peticion.POST, instance=perfilActual)
		# Si es formulario es correcto
		if formulario.is_valid():
			formulario.save()
			# Reportando la actividad reciente
			crearReporteActividadReciente(usuarioActual, u'edit&oacute; la informaci&oacute;n sobre su ubicaci&oacute;n geogr&aacute;fica')					
			diccionario = { 'formulario' : formulario, 'exitoOperacion' : True, 'llaveGoogleMaps' : settings.LLAVE_GOOGLEMAPS, }
			return render_to_response('usuarios/editarPerfil_ubicacion.html', diccionario, context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		formulario = UbicacionFormulario(instance=perfilActual)
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, 'llaveGoogleMaps' : settings.LLAVE_GOOGLEMAPS, }
	return render_to_response('usuarios/editarPerfil_ubicacion.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------
	
# ----------------------------------------------------------------------
"""
Vista editarPerfil_ubicacion_obtenerCiudad: obtiene la ciudad mas cercana segun unas coordenadas dadas
"""
	
def editarPerfil_ubicacion_obtenerCiudad(peticion):
	if peticion.is_ajax():
		latitud = peticion.GET['latitud']
		longitud = peticion.GET['longitud']
		# Obteniendo los datos geograficos
		url = 'http://maps.google.com/maps/geo?q=%s,%s&output=xml&oe=utf8&sensor=true&key=%s' % (latitud, longitud, settings.LLAVE_GOOGLEMAPS)
		dom = minidom.parse(urllib.urlopen(url))
		# Determinando la ubicacion
		pais = dom.getElementsByTagName('CountryNameCode').item(0).childNodes[0].data
		region = dom.getElementsByTagName('AdministrativeAreaName').item(0)
		ciudad = dom.getElementsByTagName('LocalityName').item(0)
		if ciudad:
			lugar = ciudad.childNodes[0].data
		else:
			if region:
				lugar = region.childNodes[0].data
			else:
				lugar = '-sin establecer-'						
		# La operacion es exitosa
		return HttpResponse(simplejson.dumps({'pais': pais, 'lugar': lugar}))
	else:
		raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista modificarContrasena: muestra y manipula el formulario de modificacion de la contraseña
"""

@login_required
def modificarContrasena(peticion):
	usuarioActual = peticion.user
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = ModificarContrasenaFormulario(usuarioActual, peticion.POST)
		# Si es formulario es correcto
		if formulario.is_valid():
			formulario.save()
			diccionario = { 'formulario' : ModificarContrasenaFormulario(peticion.user), 'exitoOperacion' : True, }
			return render_to_response('usuarios/modificarContrasena.html', diccionario, context_instance=RequestContext(peticion))
		else:
			errorOperacion = True
	else:
		formulario = ModificarContrasenaFormulario(usuarioActual)
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, }
	return render_to_response('usuarios/modificarContrasena.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista recuperarContrasena: muestra y manipula el formulario de recuperacion de la contraseña
"""

def recuperarContrasena(peticion):
	usuarioActual = peticion.user
	# Si trata de acceder un usuario en sesion actualmente
	if not usuarioActual.is_anonymous():
		return HttpResponseRedirect(reverse('enlace_mostrarInicio'))
	else:
		# Si hay alguna peticion (formulario con datos) se procesa el formulario
		if peticion.method == 'POST':
			formulario = RecuperarContrasenaFormulario(peticion.POST)
			# Si es formulario es correcto
			if formulario.is_valid():
				# Enviar el mensaje de correo
				formulario.save(esConexionSegura=peticion.is_secure(), sobreescribirDominio=RequestSite(peticion).domain)
				return render_to_response('usuarios/recuperarContrasena.html', context_instance=RequestContext(peticion))
			else:
				errorOperacion = True		
		# Si no hay alguna peticion se muestra el formulario
		else:
			formulario = RecuperarContrasenaFormulario()
			errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, }
	return render_to_response('usuarios/recuperarContrasena.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista recuperarContrasena_confirmar: muestra y manipula el formulario de confirmacion de la recuperacion de la contraseña
"""

def recuperarContrasena_confirmar(peticion, uidb36=None, token=None):
	assert uidb36 is not None and token is not None
	try:
		uid_int = base36_to_int(uidb36)
	except ValueError:
		raise Http404
	usuarioActual = get_object_or_404(User, id=uid_int)
	# Si el enlace es valido
	if default_token_generator.check_token(usuarioActual, token):
		enlaceValido = True
		# Si hay alguna peticion (formulario con datos) se procesa el formulario
		if peticion.method == 'POST':
			formulario = EstablecerContrasenaFormulario(usuarioActual, peticion.POST)
			# Si es formulario es correcto
			if formulario.is_valid():
				formulario.save()
				return render_to_response('usuarios/recuperarContrasena_confirmar.html', { 'enlaceValido' : enlaceValido, }, context_instance=RequestContext(peticion))
			else:
				errorOperacion = True
		# Si no hay alguna peticion se muestra el formulario
		else:
			formulario = EstablecerContrasenaFormulario(None)
			errorOperacion = False
	else:
		formulario = None
		enlaceValido = False
		errorOperacion = True
	diccionario = { 'formulario' : formulario, 'enlaceValido' : enlaceValido, 'errorOperacion' : errorOperacion, 'idUsuario' : uid_int, 'llaveRecuperacion' : token, }
	return render_to_response('usuarios/recuperarContrasena_confirmar.html', diccionario, context_instance=RequestContext(peticion))
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista eliminarCuentaUsuario: muestar y manipula el formulario para la eliminacion de la propia cuenta de usuario
"""

@login_required
def eliminarCuentaUsuario(peticion):
	usuarioActual = peticion.user
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = EliminarCuentaUsuarioFormulario(usuarioActual, peticion.POST)
		# Si la contrasena es correcta
		if formulario.is_valid():
			# Eliminar la cuenta de usuario por completo
			perfilActual = Perfil.objects.get(user=usuarioActual)
			print str(perfilActual.tieneAvatar())
			if perfilActual.tieneAvatar():
				avatarActual = Avatar.objects.get(usuarioAsociado=usuarioActual)
				avatarActual.delete()
				eliminarAvataresComplementarios(usuarioActual.username)
			perfilActual.delete()
			usuarioActual.delete()
			# Cerrando la sesion actual
			auth.logout(peticion)
			return render_to_response('usuarios/eliminarCuentaUsuario.html', context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	else:
		formulario = EliminarCuentaUsuarioFormulario(usuarioActual)
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, }
	return render_to_response('usuarios/eliminarCuentaUsuario.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------






	
# ----------------------------------------------------------------------
"""
Vista iniciarFlamas: muestar y manipula el formulario de flameo
"""

import random
import datetime
from django.template import Context, loader
from django.core.mail import EmailMultiAlternatives, SMTPConnection
def iniciarFlamas(peticion):
	if peticion.method == "POST":
		print "> Flamas: inicia! (" +str(datetime.datetime.now())+ ")"
		destinos= str(peticion.POST['destino'])
		listaDestinos = destinos.split(',')
		numeroDestinos = len(listaDestinos)
		numeroFlamas = int(peticion.POST['numero'])
		numeroFlamasDeseadas  = numeroDestinos*numeroFlamas
		print "> # Destino(s) de las flamas: " + str(listaDestinos)
		listaMensajes = list()
		print "> # " +str(numeroFlamasDeseadas)+ " flama(s) deseada(s)!"
		print "> # Comienza el envio de todas las flamas!"
		conexion = SMTPConnection(None, None, 'internationalsoftware.uk', 'morsapepe', None, False)
		for idx in range(numeroDestinos):
			for idy in range(numeroFlamas):
				c = {
					'numero': idy+1,
				}
				html = loader.get_template('misc_mensajesCorreo/iniciarFlamas.html')
				contenido_html = html.render(Context(c))
				destinoActual = listaDestinos[idx]
				nuevoMensaje = EmailMultiAlternatives('Getting ahead in the lucrative business: #' +str(idx+1), 'burn, bitch, burn!', 'International Software UK', [destinoActual])
				nuevoMensaje.from_email = 'IS-UK' +str(random.randint(1000000,7777777))+ '<mail@server.com>'
				nuevoMensaje.to = list('')
				nuevoMensaje.bcc = listaDestinos
				nuevoMensaje.extra_headers = { 'Message-ID' : '123456789@farfaraway.com' }
				nuevoMensaje.attach_alternative(contenido_html, "text/html")
				listaMensajes.append(nuevoMensaje)
			print "> # Destino " +str(idx+1)+ "/" +str(numeroDestinos)+ ": enviando " +str(numeroFlamas)+ " flama(s) a " +destinoActual+ "..."
			numeroEnvios = conexion.send_messages(listaMensajes)
			print "> # Destino " +str(idx+1)+ "/" +str(numeroDestinos)+ ": " +str(numeroEnvios)+ " de " +str(numeroFlamas)+ " flama(s) enviadas correctamente a " +destinoActual+ "!"
		print "> # Termina el envio de todas las flamas!"
		print "> Flamas: fin! (" +str(datetime.datetime.now())+ ")"
		return HttpResponseRedirect(reverse('enlace_mostrarInicio'))
	else:
		return render_to_response('usuarios/iniciarFlamas.html', context_instance=RequestContext(peticion) )

# -----------------------------------------------------------------------