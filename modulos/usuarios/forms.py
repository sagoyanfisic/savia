# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/usuarios/forms.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 09:26
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import os
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django import forms
from email.MIMEImage import MIMEImage
from django.contrib.auth.forms import PasswordResetForm
from savia.modulos.usuarios.models import Perfil
from savia.modulos.utilidades.utils import *

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales para este archivo """

TIPOS_IMAGENES_VALIDAS = [ '.jpg', '.jpeg', '.png', '.gif' ]

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase RegistroFormulario: define el formulario para el perfil de un usuario
Entradas: hereda de Form, ninguna
"""

class RegistroFormulario(forms.Form):

	nombreElegido = forms.CharField()
	nombres= forms.CharField()
	apellidos = forms.CharField()
	correo = forms.EmailField()
	contrasena1 = forms.CharField(widget=forms.PasswordInput)
	contrasena2 = forms.CharField(widget=forms.PasswordInput)

	"""
	Funcion clean_nombreElegido: valida el formulario de tipo RegistroFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""	
	def clean_nombreElegido(self):
		nombreElegido = self.cleaned_data.get('nombreElegido')
		if len(nombreElegido) >= 5:
			if not set(nombreElegido).issubset('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_'):
				self._errors['nombreElegido'] = u'Digita caracteres v&aacute;lidos (letras, n&uacute;meros y "_").'
			if User.objects.filter(username__iexact=nombreElegido).count() == 0:
				return nombreElegido
			else:
				self._errors['nombreElegido'] = u'El nombre de usuario elegido no está disponible.'	
		else:
			self._errors['nombreElegido'] = u'Digita por lo menos 5 caracteres.'					
	
	"""
	Funcion clean_contrasena2: valida el formulario de tipo RegistroFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""				
	def clean_contrasena2(self):
		contrasena2 = self.cleaned_data.get('contrasena2')
		if len(self.cleaned_data.get('contrasena1')) >= 5:
			if self.cleaned_data.get('contrasena1') == contrasena2:
				contrasena = self.cleaned_data.get('contrasena2')
				return contrasena2
			else:
				self._errors['contrasena2'] = u'Las contraseñas digitadas no coinciden.'
		else:
			self._errors['contrasena1'] = u'Digita por lo menos 5 caracteres.'

	"""
	Funcion clean_correo: valida el formulario de tipo RegistroFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""			
	def clean_correo(self):
		correo = self.cleaned_data.get('correo')
		try:
			User.objects.get(email=correo)
			self._errors['correo'] = u'La dirección de correo electrónico digitada ya ha sido registrada.'
		except User.DoesNotExist:
			return correo

	"""
	Funcion save: procesa el formulario de tipo RegistroFormulario, enviando el mensaje de activacion por correo electronico
	Entradas: el mismo formulario, esConexionSegura:boolean, sobreescribirDominio:string
	Salidas: ninguna
	"""
	def save(self, esConexionSegura=False, sobreescribirDominio=None):
		# Para cada usuario que haya solicitado la recuperacion de la contraseña
		correoActual = self.cleaned_data.get('correo')
		usuarioActual = User.objects.get(email=correoActual, is_active=False)
		# Envia el mensaje de correo electronico a traves de la cuenta estandar definida en settings.py
		enviarMensajeCorreo('activarCuentaUsuario_mensaje', usuarioActual, correoActual, u'activar mi cuenta de usuario', esConexionSegura, sobreescribirDominio, '', '')					

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase PerfilFormulario: define el formulario para el perfil de un usuario
Entradas: hereda de ModelForm, ninguna
"""

class PerfilFormulario(forms.ModelForm):

	# Valores meta de la clase Perfil
	class Meta:
		model = Perfil
		exclude = ( 'user', 'numeroVisitas', 'temaPreferido', 'pais', 'lugar', 'latitud', 'longitud', )
	
	"""
	Funcion clean: valida el formulario de tipo PerfilFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""
	def clean(self):
		sexo = self.cleaned_data.get('sexo')
		fechaNacimiento = self.cleaned_data.get('fechaNacimiento')
		url = self.cleaned_data.get('url')
		acerca = self.cleaned_data.get('acerca')
		if not sexo:
			self._errors['sexo'] = u'Selecciona un sexo válido'
		if not fechaNacimiento:
			self._errors['fechaNacimiento'] = u'Introduce una fecha válida'
		if not url:
			self._errors['url'] = u'Digita una URL válida'
		if not acerca:
			self._errors['acerca'] = u'Digita texto válido'
		return self.cleaned_data

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase AvatarFormulario: define el formulario para subir la imagen que se desea como avatar
Entradas: hereda de Form, ninguna
"""

class AvatarFormulario(forms.Form):

	imagen = forms.ImageField(label=u'Imagen', required=False)

	"""
	Funcion clean: valida el formulario de tipo AvatarFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""
	def clean(self):
		imagen = self.cleaned_data.get('imagen')
		nombreImagen = str(imagen)
		nombreArchivo, extensionArchivo = os.path.splitext(nombreImagen)
		# Comprobando que el archivo tenga extension de imagen valida
		if extensionArchivo in TIPOS_IMAGENES_VALIDAS:
			formatoInvalido = False
		else:
			formatoInvalido = True
		if not imagen or formatoInvalido:
			raise forms.ValidationError([u'Selecciona una imagen con formato válido'])
		return self.cleaned_data

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase RecortarImagenFormulario: define el formulario para la gestion de la imagen de avatar de un usuario
Entradas: hereda de forms.Form, ninguna
"""

class RecortarImagenFormulario(forms.Form):

	arriba = forms.IntegerField(widget=forms.HiddenInput)
	abajo = forms.IntegerField(widget=forms.HiddenInput)
	izquierda = forms.IntegerField(widget=forms.HiddenInput)
	derecha = forms.IntegerField(widget=forms.HiddenInput)

	"""
	Funcion clean: valida el formulario de tipo RecortarImagenFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""
	def clean(self):
		izquierda = int(self.cleaned_data.get('izquierda'))
		derecha = int(self.cleaned_data.get('derecha'))	
		if derecha-izquierda < 96:
			raise forms.ValidationError(u'Selecciona una región de dimensiones válidas.')
		else:
			return self.cleaned_data

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase UbicacionFormulario: define el formulario para la gestion los datos de la ubicacion de un usuario
Entradas: hereda de ModelForm, ninguna
"""

class UbicacionFormulario(forms.ModelForm):

	# Valores meta de la clase Perfil
	class Meta:
		model = Perfil
		fields = ( 'pais', 'lugar', 'latitud', 'longitud', )

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase EstablecerContrasenaFormulario: define el formulario para establecer la contraseña de un usuario
Entradas: hereda de ModelForm, ninguna
"""

class EstablecerContrasenaFormulario(forms.Form):

	nuevaContrasena1 = forms.CharField(label=u'Nueva contraseña', widget=forms.PasswordInput)
	nuevaContrasena2 = forms.CharField(label=u'Nueva contraseña (otra vez)', widget=forms.PasswordInput)

	"""
	Funcion __init__: inicializa una instancia de la clase EstablecerContrasenaFormulario
	Entradas: el mismo formulario, usuarioActual:objeto
	Salidas: el mismo formulario
	"""
	def __init__(self, usuarioActual, *args, **kwargs):
		self.usuarioActual = usuarioActual
		super(EstablecerContrasenaFormulario, self).__init__(*args, **kwargs)

	"""
	Funcion clean_new_password2: valida el formulario de tipo EstablecerContrasenaFormulario
	Entradas: el mismo formulario
	Salidas: string
	"""
	def clean_nuevaContrasena2(self):
		contrasena1 = self.cleaned_data.get('nuevaContrasena1')
		contrasena2 = self.cleaned_data.get('nuevaContrasena2')
		if contrasena1 and contrasena2:
			if len(contrasena1) < 5:
				raise forms.ValidationError([u'Digita al menos 5 caracteres'])
			else:
				if contrasena1 != contrasena2:
					raise forms.ValidationError([u'Las contraseñas digitadas no coinciden.'])
		return contrasena2

	"""
	Funcion save: almacena el formulario de tipo EstablecerContrasenaFormulario
	Entradas: el mismo formulario, commit:boolean
	Salidas: objeto
	"""		
	def save(self, commit=True):
		self.usuarioActual.set_password(self.cleaned_data['nuevaContrasena1'])
		if commit:
			self.usuarioActual.save()
		return self.usuarioActual

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase ModificarContrasenaFormulario: define el formulario para la modificacion de la contraseña de un usuario
Entradas: hereda de ModelForm, ninguna
"""
 
class ModificarContrasenaFormulario(EstablecerContrasenaFormulario):

	contrasenaActual = forms.CharField(label=u'Contraseña actual', widget=forms.PasswordInput)
	
	"""
	Funcion clean_contrasenaActual: valida el formulario de tipo ModificarContrasenaFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""
	def clean_contrasenaActual(self):
		contrasenaActual = self.cleaned_data['contrasenaActual']
		if not self.usuarioActual.check_password(contrasenaActual):
			raise forms.ValidationError([ u'La contraseña actual es incorrecta.'])
		return contrasenaActual

# ----------------------------------------------------------------------
  
# ----------------------------------------------------------------------
"""
Clase RecuperarContrasenaFormulario: define el formulario para iniciar el proceso de recuperacion de la contraseña via correo electronico
Entradas: hereda de PasswordResetForm, ninguna
"""

class RecuperarContrasenaFormulario(PasswordResetForm):

	"""
	Funcion clean: valida el formulario de tipo RecuperarContrasenaFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""			
	def clean_email(self):
		correo = self.cleaned_data.get('email')
		if not correo:
			raise forms.ValidationError([u'La dirección de correo electrónico es inválida.'])
		else:
			try:
				User.objects.get(email=correo)
				return correo
			except User.DoesNotExist:
				raise forms.ValidationError([u'La dirección de correo electrónico digitada no se encuentra registrada.'])

	"""
	Funcion save: procesa el formulario de tipo RecuperarContrasenaFormulario, enviando el mensaje de recuperacion por correo electronico
	Entradas: el mismo formulario, domain_override:string, use_https:boolean
	Salidas: ninguna
	"""
	def save(self, esConexionSegura=False, sobreescribirDominio=None):
		# Para cada usuario que haya solicitado la recuperacion de la contraseña
		correoActual = self.cleaned_data.get('email')
		usuarioActual = User.objects.get(email=correoActual)
		# Envia el mensaje de correo electronico a traves de la cuenta estandar definida en settings.py
		enviarMensajeCorreo('recuperarContrasena_mensaje', usuarioActual, correoActual, u'recuperar mi contraseña', esConexionSegura, sobreescribirDominio, '', '')

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase EliminarCuentaUsuarioFormulario: define el formulario para la eliminacion de una cuenta de un usuario
Entradas: hereda de ModelForm, ninguna
"""
 
class EliminarCuentaUsuarioFormulario(forms.Form):

	contrasenaActual = forms.CharField(label=u'Contraseña actual', widget=forms.PasswordInput)
	
	"""
	Funcion __init__: inicializa una instancia de la clase EstablecerContrasenaFormulario
	Entradas: el mismo formulario, usuarioActual:objeto
	Salidas: el mismo formulario
	"""
	def __init__(self, usuarioActual, *args, **kwargs):
		self.usuarioActual = usuarioActual
		super(EliminarCuentaUsuarioFormulario, self).__init__(*args, **kwargs)	
	
	"""
	Funcion clean_contrasenaActual: valida el formulario de tipo ModificarContrasenaFormulario
	Entradas: el mismo formulario
	Salidas: el mismo formulario
	"""
	def clean_contrasenaActual(self):
		contrasenaActual = self.cleaned_data['contrasenaActual']
		if not self.usuarioActual.check_password(contrasenaActual):
			raise forms.ValidationError([ u'La contraseña actual es incorrecta.'])
		return contrasenaActual

# ----------------------------------------------------------------------