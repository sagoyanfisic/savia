# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/general/forms.py
Julian Perez
Ultima modificacion: Abril 21 de 2009, 09:26
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from email.MIMEImage import MIMEImage
from savia.modulos.relaciones.models import Mensaje
from savia.modulos.utilidades.utils import *

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales para este archivo """

TIPOS_MENSAJE_CONTACTO = ( ('p', 'Problema'), ('i', 'Inquietud'), ('s', 'Sugerencia'), )

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase ContactoFormulario: define el formulario para enviar un mensaje de contactocon el administrador
Entradas: hereda de Forms, ninguna
"""

class ContactoFormulario(forms.Form):
	
	remitente = forms.CharField()
	correoRemitente =   forms.EmailField()
	tituloMensaje = forms.CharField()
	tipoMensaje = forms.CharField(widget=forms.Select(choices=TIPOS_MENSAJE_CONTACTO))
	contenidoMensaje = forms.CharField(widget=forms.Textarea())
	
	"""
	Funcion clean_tituloMensaje: valida el formulario de tipo ContactoFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""	
	def clean_tituloMensaje(self):
		tituloMensaje = self.cleaned_data.get('tituloMensaje')
		if len(tituloMensaje) > 55:
			self._errors['tituloMensaje'] = u'Digita como máximo 55 caracteres.'	
		else:
			return tituloMensaje

	"""
	Funcion clean_contenidoMensaje: valida el formulario de tipo ContactoFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""	
	def clean_contenidoMensaje(self):
		contenidoMensaje = self.cleaned_data.get('contenidoMensaje')
		if len(contenidoMensaje) > 555:
			self._errors['contenidoMensaje'] = u'Digita como máximo 555 caracteres.'	
		else:
			return contenidoMensaje			
	
	"""
	Funcion save: procesa el formulario de tipo ContactoFormulario, enviando el mensaje de contacto correspondiente
	Entradas: el mismo formulario, esConexionSegura:boolean, sobreescribirDominio:string
	Salidas: ninguna
	"""
	def save(self, usuarioActual, esConexionSegura=False, sobreescribirDominio=None):
		tituloMensaje = self.cleaned_data.get('tituloMensaje')
		tipoMensaje = obtenerValorTupla(TIPOS_MENSAJE_CONTACTO, self.cleaned_data.get('tipoMensaje'))
		contenidoMensaje = self.cleaned_data.get('contenidoMensaje')
		# Si es un usuario sin sesion actualmente quien desea enviar el mensaje
		if usuarioActual.is_anonymous():
			remitente = self.cleaned_data.get('remitente')
			correoRemitente = self.cleaned_data.get('correoRemitente')
			# Creando un usuario anonimo en la marcha para enviar el comprobante de contacto
			usuarioActual = User.objects.get(username=settings.NOMBRE_USUARIO_ANONIMO)
			usuarioActual.username = remitente
			usuarioActual.password = remitente
			usuarioActual.last_login = datetime.datetime.now()
			usuarioActual.first_name = remitente
			# Contenido del mensaje
			contenidoMensaje_html = '<b>T&iacute;tulo:</b> ' +tituloMensaje+ '<br/><b>Tipo:</b> ' +tipoMensaje.lower()+ '<br/><b>Mensaje:</b> ' +contenidoMensaje
			contenidoMensaje_txt = 'Titulo: ' +tituloMensaje+ '\nTipo: ' +tipoMensaje.lower()+ '\nMensaje: ' +contenidoMensaje
			contenidoMensaje_interno = 'Remitido por ' +remitente+ ' (' +correoRemitente+ '):\n' +contenidoMensaje
			# Envia un mensaje de correo como comprobante del contacto
			enviarMensajeCorreo('comprobanteContacto_mensaje', usuarioActual, correoRemitente, u'comprobante de contacto', esConexionSegura, sobreescribirDominio, contenidoMensaje_html, contenidoMensaje_txt)
		# Si es un usuario registrado quien desea enviar el mensaje
		else:
			contenidoMensaje_interno = contenidoMensaje
		# Enviar el mensaje de contacto al administrador
		usuarioAdministrador = User.objects.get(username=settings.NOMBRE_USUARIO_ADMIN)
		tituloMensaje_interno = 'mensaje de contacto (' +tipoMensaje.lower()+ ') | ' +tituloMensaje
		mensajeActual = Mensaje(usuarioOrigen=usuarioActual, usuarioDestino=usuarioAdministrador, titulo=tituloMensaje_interno, contenido=contenidoMensaje_interno, esImportante=True)
		mensajeActual.save()
	
# ----------------------------------------------------------------------