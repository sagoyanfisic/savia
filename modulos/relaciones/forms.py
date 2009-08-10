# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/relaciones/forms.py
Julian Perez
Ultima modificacion: Agosto 03 de 2009, 09:26
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
from savia.modulos.usuarios.models import GENEROS, PAISES_DISPONIBLES
from savia.modulos.relaciones.models import retornarListaAmigos

# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
"""
Clase SeleccionarUsuarioDestino: define el campo de seleccion del usuario destino
Entradas: hereda de Forms, ninguna
"""

class SeleccionarUsuarioDestino(forms.ModelChoiceField):

	"""
	Funcion label_from_instance: retorna la representacion por defecto de la clase SeleccionarUsuarioDestino
	Entradas: el mismo campo, usuarioActual:objeto
	Salidas: string
	"""
	def label_from_instance(self, usuarioActual):
		return usuarioActual.get_full_name()+ ' --- ' +usuarioActual.username

# ----------------------------------------------------------------------		  

# ----------------------------------------------------------------------
"""
Clase EnviarMensajeFormulario: define el formulario para enviar un nuevo mensaje
Entradas: hereda de Forms, ninguna
"""

class EnviarMensajeFormulario(forms.Form):
	
	usuarioDestino = forms.CharField()
	tituloMensaje = forms.CharField(label=u'Título')
	contenidoMensaje = forms.CharField(label=u'Contenido', widget=forms.Textarea())
	
	"""
	Funcion __init__: inicializa una instancia de la clase EnviarMensajeFormulario
	Entradas: el mismo formulario, usuarioActual:objeto
	Salidas: el mismo formulario
	"""
	def __init__(self, usuarioActual, *args, **kwargs):
		self.usuarioActual = usuarioActual
		super(EnviarMensajeFormulario, self).__init__(*args, **kwargs)
		# Determinando los posibles usuarios de destino
		if self.usuarioActual.is_staff:
			listaUsuariosAdecuados = User.objects.all().exclude(username=settings.NOMBRE_USUARIO_ADMIN).exclude(username=settings.NOMBRE_USUARIO_ANONIMO)
			self.fueCreado = True
			# Actualizando el campo de seleccion del usuario de destino
			self.fields['usuarioDestino'] = SeleccionarUsuarioDestino(label=u'Usuario de destino', queryset=listaUsuariosAdecuados)
		else:
			listaUsuariosAdecuados, self.fueCreado = retornarListaAmigos(self.usuarioActual)
			# Actualizando el campo de seleccion del usuario de destino
			self.fields['usuarioDestino'] = forms.CharField(label=u'Usuario de destino', widget=forms.Select(choices=listaUsuariosAdecuados))
	
	"""
	Funcion clean_tituloMensaje: valida el formulario de tipo EnviarMensajeFormulario
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
	Funcion clean_contenidoMensaje: valida el formulario de tipo EnviarMensajeFormulario
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
	Funcion save: procesa el formulario de tipo EnviarMensajeFormulario, enviando el mensaje de contacto correspondiente
	Entradas: el mismo formulario
	Salidas: ninguna
	"""
	def save(self):
		tituloMensaje = self.cleaned_data['tituloMensaje']
		contenidoMensaje = self.cleaned_data['contenidoMensaje']
		if self.usuarioActual.is_staff:
			usuarioDestino = self.cleaned_data['usuarioDestino']
		else:
			usuarioDestino = User.objects.get(id=self.cleaned_data['usuarioDestino'])
		mensajeActual = Mensaje(usuarioOrigen=self.usuarioActual, usuarioDestino=usuarioDestino, titulo=tituloMensaje, contenido=contenidoMensaje)
		mensajeActual.save()
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase EnviarCorreoFormulario: define el formulario para enviar un nuevo mensaje
Entradas: hereda de Forms, ninguna
"""

class EnviarCorreoFormulario(forms.Form):
	
	usuarioDestino = forms.CharField(label=u'Usuario de destino')
	correoDestino = forms.EmailField(label=u'Dirección de correo electrónico de destino')
	contenidoMensaje = forms.CharField(label=u'Contenido', widget=forms.Textarea())

	"""
	Funcion clean_contenidoMensaje: valida el formulario de tipo EnviarCorreoFormulario
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
	Funcion save: procesa el formulario de tipo EnviarCorreoFormulario, enviando el mensaje de contacto correspondiente
	Entradas: el mismo formulario
	Salidas: ninguna
	"""
	def save(self, esConexionSegura=False, sobreescribirDominio=None):
		usuarioDestino = self.cleaned_data['usuarioDestino']
		correoDestino = self.cleaned_data['correoDestino']
		contenidoMensaje = self.cleaned_data['contenidoMensaje']
		# Creando un usuario anonimo en la marcha para enviar el comprobante de contacto
		usuarioActual = User.objects.get(username=settings.NOMBRE_USUARIO_ANONIMO)
		usuarioActual.username = usuarioDestino
		usuarioActual.password = usuarioDestino
		usuarioActual.last_login = datetime.datetime.now()
		usuarioActual.first_name = usuarioDestino	
		# Envia un mensaje de correo como comprobante del contacto
		enviarMensajeCorreo('respuestaAdministrador_mensaje', usuarioActual, correoDestino, u'respuesta del administrador', esConexionSegura, sobreescribirDominio, contenidoMensaje, contenidoMensaje)
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase ResponderMensajeFormulario: define el formulario para responder un mensaje
Entradas: hereda de Forms, ninguna
"""

class ResponderMensajeFormulario(forms.Form):
	
	respuestaMensaje = forms.CharField(label=u'Respuesta', widget=forms.Textarea())
	
	"""
	Funcion __init__: inicializa una instancia de la clase ResponderMensajeFormulario
	Entradas: el mismo formulario, mensajeReferencia:objeto
	Salidas: el mismo formulario
	"""
	def __init__(self, mensajeReferencia, *args, **kwargs):
		self.mensajeReferencia = mensajeReferencia
		super(ResponderMensajeFormulario, self).__init__(*args, **kwargs)	

	"""
	Funcion clean_respuestaMensaje: valida el formulario de tipo ResponderMensajeFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""	
	def clean_respuestaMensaje(self):
		respuestaMensaje = self.cleaned_data.get('respuestaMensaje')
		if len(respuestaMensaje) > 555:
			self._errors['respuestaMensaje'] = u'Digita como máximo 555 caracteres.'	
		else:
			return respuestaMensaje			
	
	"""
	Funcion save: procesa el formulario de tipo ResponderMensajeFormulario, enviando el mensaje de contacto correspondiente
	Entradas: el mismo formulario, esConexionSegura:boolean, sobreescribirDominio:string
	Salidas: ninguna
	"""
	def save(self, esConexionSegura=False, sobreescribirDominio=None):
		respuestaMensaje = self.cleaned_data['respuestaMensaje'] + ' *** (' +self.mensajeReferencia.usuarioOrigen.username+ ' dijo: ' +self.mensajeReferencia.contenido+ ')'
		tituloRespuesta = '[RE]: ' +self.mensajeReferencia.titulo
		mensajeActual = Mensaje(usuarioOrigen=self.mensajeReferencia.usuarioDestino, usuarioDestino=self.mensajeReferencia.usuarioOrigen, titulo=tituloRespuesta, contenido=respuestaMensaje)
		mensajeActual.save()
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase BusquedaUsuariosFormulario: define el formulario para buscar usuarios
Entradas: hereda de Forms, ninguna
"""

class BusquedaUsuariosFormulario(forms.Form):
	
	nombreUsuario = forms.CharField(label=u'Nombre de usuario', initial='-sin establecer-')
	sexo = forms.CharField(label=u'Sexo', widget=forms.Select(choices=GENEROS))
	pais = forms.CharField(label=u'País', widget=forms.Select(choices=PAISES_DISPONIBLES))
	lugar = forms.CharField(u'Lugar', initial='-sin establecer-')	
	
# ----------------------------------------------------------------------