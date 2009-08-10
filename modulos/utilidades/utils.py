# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/utilidades/utils.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 09:13
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import os, glob
import time
import datetime
import sha
import Image, ImageColor, ImageFont, ImageDraw
from random import choice
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.utils.http import int_to_base36
from django.template import Context, loader

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales para este archivo """

codigoSalt = settings.SECRET_KEY[:20]

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearArchivoVariablesEntornoJS: crea un archivo Javascript con las principales variebles de entorno, relativas a settings.py
Entradas: nombreArchivoSalida:string
Salidas: ninguna
"""

def crearArchivoVariablesEntornoJS(nombreArchivoSalida):
	archivoSalida = open(settings.RUTA_JS+nombreArchivoSalida+ '.js', 'w')
	estampaTiempo = str(datetime.datetime.now())
	cadenaEncabezado= '/**\n----------------------------------------------------------------------\n---\nsavia/media/js/' +nombreArchivoSalida+ '.js\nArchivo autogenerado\n' +estampaTiempo+ '\n---\n----------------------------------------------------------------------\n**/\n\n\n\n'
	contenidoVariables = ''
	contenidoVariables += 'NOMBRE_APLICACION = "' +settings.NOMBRE_APLICACION+ '";\n'
	contenidoVariables += 'URL_CAMBIAR_TEMA = "' +settings.URL_PREFIJO+reverse('enlace_cambiarTema')+ '";\n'
	contenidoVariables += 'URL_PREFIJO = "' +settings.URL_PREFIJO+ '";\n'
	contenidoVariables += 'URL_MEDIA = "' +settings.MEDIA_URL+ '";\n'
	contenidoVariables += 'URL_IMG = "' +settings.URL_IMG+ '";\n'
	contenidoVariables += 'URL_INICIO = "' +settings.URL_PREFIJO+ '";\n'
	contenidoVariables += 'URL_TERMINAR_SESION = "' +settings.URL_PREFIJO+reverse('enlace_terminarSesion')+ '";\n'
	contenidoVariables += 'URL_OBTENER_CIUDAD = "' +settings.URL_PREFIJO+reverse('enlace_editarPerfil_ubicacion_obtenerCiudad')+ '";\n'
	cadenaCuerpo = '// ----------------------------------------------------------------------\n\n' +contenidoVariables+ '\n// ----------------------------------------------------------------------'
	archivoSalida.write(cadenaEncabezado+cadenaCuerpo)
	return ''

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion calcularEdad: calcula la edad de un usuario a partir de la fecha de nacimiento
Entradas: objeto(datetime.datime)
Salidas: int
"""

def calcularEdad(fechaNacimiento):
	if fechaNacimiento:
		fechaInicio = datetime.datetime.strptime(str(fechaNacimiento), '%Y-%m-%d')
		# Calculando la diferencia de tiempo entre el dia de nacimiento y hoy
		diferencia = datetime.datetime.today() - fechaInicio
		# Calculando los años de diferencia
		edad = diferencia.days/365
		if edad>0 and edad<232:
			return str(edad)+ u' años'
	return u'Entre 0 y 777 años'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearCaptcha: crea un codigo captcha y la imagen que lo representa
Entradas: ipPeticion:string
Salidas: string, string
"""

def crearCaptcha():
	# Generando el codigo del captcha
	alfabetoElegido = '1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
	textoImagen = ''.join([choice(alfabetoElegido) for i in range(5)])
	# Generando el codigo hash para el codigo captcha generado
	codigoImagen = sha.new(codigoSalt+textoImagen).hexdigest()
	# Determinando el tamaño de la imagen
	anchoImagen = 33 + (5*25)	
	# Creando la imagen del captcha
	imagenCaptcha = Image.new('RGB', (anchoImagen,47), '#EEEEEE')
	dibujarImagen = ImageDraw.Draw(imagenCaptcha)
	fuenteCaptcha = ImageFont.truetype(settings.RUTA_FNT+ 'nervous.ttf', 33)
	colorFuente = ImageColor.getrgb('#804000')
	dibujarImagen.text((3,0), textoImagen, font=fuenteCaptcha, fill=colorFuente)
	# Almacenando la imagen captcha generada
	captchaFinal = settings.RUTA_IMGTMP+codigoImagen+ '.png'
	captchaFinal_nombre = 'tmp/' +codigoImagen+ '.png'
	imagenCaptcha.save(captchaFinal, 'PNG')
	return codigoImagen, captchaFinal_nombre
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion verificarCaptcha: verifica si el captcha que ha sido digitado es el mismo que habia sido generado
Entradas: captchaGenerado:string, captchaDigitado:string
Salidas: boolean
"""

def verificarCaptcha(captchaGenerado, captchaDigitado):
	if captchaGenerado == sha.new(codigoSalt+captchaDigitado).hexdigest():
		return True
	else:
		return False

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion eliminarCaptcha: elimina la imagen del captcha especificado
Entradas: captchaGenerado:string
Salidas: ninguna
"""

def eliminarCaptcha(captchaGenerado):
	try:
		os.remove(settings.RUTA_IMGTMP+captchaGenerado+ '.png')
	except:
		pass

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion eliminarImagenesAsociadas: elimina las imagenes asociadas al usuario
Entradas: nombreUsuario:string
Salidas: ninguna
"""

def eliminarImagenesAsociadas(nombreUsuario):
	try:
		rutaDestino_avatar = os.path.join(settings.RUTA_AVATARES, nombreUsuario+ '*.jpg')
		rutaDestino_dce = os.path.join(settings.RUTA_IMGDCE, nombreUsuario+ '*.jpg')
		for archivoEncontrado in glob.glob(rutaDestino_avatar):
			os.remove(archivoEncontrado)
		for archivoEncontrado in glob.glob(rutaDestino_dce):
			os.remove(archivoEncontrado)			
	except:
		pass

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion enviarMensajeCorreo: envia un mensaje de correo electronico
Entradas: nombrePlantilla:string, usuarioAsociado:objeto, direccionDestino:string, tituloMensaje:string, esConexionSegura:boolean, sobreescribirDominio:objeto, contenidoMensaje_html:string, contenidoMensaje_texto:string
Salidas: ninguna
"""

def enviarMensajeCorreo(nombrePlantilla, usuarioAsociado, direccionDestino, tituloMensaje, esConexionSegura, sobreescribirDominio, contenidoMensaje_html, contenidoMensaje_texto):
	# Calcula el nombre del sitio y del dominio actual
	if not sobreescribirDominio:
		sitioActual = Site.objects.get_current()
		nombreSitioActual = sitioActual.name
		dominioSitioActual = sitioActual.domain
	else:
		nombreSitioActual = dominioSitioActual = sobreescribirDominio
	# Cargando las plantillas en modo HTML y modo texto plano
	html = loader.get_template('correo/' +nombrePlantilla+ '.html')
	texto = loader.get_template('correo/' +nombrePlantilla+ '.txt')
	# Variables de contexto para las plantillas
	contexto = {
		'nombreAplicacion' : settings.NOMBRE_APLICACION,
		'versionActual' : settings.VERSION_APLICACION,
		'rutaLogo' : settings.URL_IMG+ 'savia_logo_izq.gif',
		'rutaInicio' : reverse('enlace_mostrarInicio'),
		'usuarioActual': usuarioAsociado.username,
		'usuarioActual_nombre': usuarioAsociado.first_name,
		'fechaHoraActual' : datetime.datetime.now(),
		'protocolo': esConexionSegura and 'https' or 'http',
		'dominio': dominioSitioActual,
		'uid': int_to_base36(usuarioAsociado.id),
		'token': default_token_generator.make_token(usuarioAsociado),
		'contenidoMensaje_html' : contenidoMensaje_html,
		'contenidoMensaje_texto' : contenidoMensaje_texto,
	}
	contenido_texto = texto.render(Context(contexto))
	contenido_html = html.render(Context(contexto))
	# Construye el mensaje de correo electronico con base en lla plantilla de texto plano y adjuntando la plantilla HTML
	mensaje = EmailMultiAlternatives(tituloMensaje+ ' | ' +settings.NOMBRE_APLICACION, contenido_texto, settings.NOMBRE_CORREO, [direccionDestino])
	#mensaje.send()
	mensaje.attach_alternative(contenido_html, 'text/html')
	# Envia el mensaje de correo electronico a traves de la cuenta estandar definida en settings.py
	try:
		mensaje.send()
	except:
		pass

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearImagenDireccionCorreo: crea un codigo captcha y la imagen que lo representa
Entradas: usuarioActual:objeto
Salidas: string
"""

def crearImagenDireccionCorreo(usuarioActual):
	# Obteniendo los datos del usuario actual
	nombreUsuario = usuarioActual.username
	direccionCorreo = usuarioActual.email
	# Determinando el tamaño de la imagen
	longitudDireccionCorreo = len(direccionCorreo)
	anchoImagen = 13 + (longitudDireccionCorreo*7)
	# Creando la imagen de la direccion de correo
	imagenDireccionCorreo = Image.new('RGB', (anchoImagen,19), '#EEEEEE')
	dibujarImagen = ImageDraw.Draw(imagenDireccionCorreo)
	fuenteImagen = ImageFont.truetype(settings.RUTA_FNT+ 'weezer.ttf', 12)
	colorFuente = ImageColor.getrgb('#000000')
	dibujarImagen.text((3,0), direccionCorreo, font=fuenteImagen, fill=colorFuente)
	# Almacenando la imagen captcha generada
	imagenFinal = settings.RUTA_IMGDCE+nombreUsuario+ '.png'
	imagenFinal_nombre = 'dce/' +nombreUsuario+ '.png'
	imagenDireccionCorreo.save(imagenFinal, 'PNG')
	return imagenFinal_nombre

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion obtenerValorTupla: optiene el valor de una lista de tuplas tipo ( ('llaveActual', 'valorActual'), ... )
Entradas: tuplaEntrada:lista, clave:string
Salidas: string
"""

def obtenerValorTupla(tuplaEntrada, clave):
	for elementoActual in tuplaEntrada:
		llaveActual = elementoActual[0]
		valorActual = elementoActual[1]
		if llaveActual == clave:
			return valorActual
	return ''

# ----------------------------------------------------------------------