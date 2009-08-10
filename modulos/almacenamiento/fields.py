# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/almacenamiento/fields.py
Julian Perez
Ultima modificacion: Marzo 31 de 2009, 09:26
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

from os.path import *
from django import forms

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Clase ArchivoErroresValidacion: define la clase de los errores de validacion de un formulario de archivos
Entradas: hereda de ValidationError, ninguna
"""

class ArchivoErroresValidacion(forms.ValidationError):

	"""
	Funcion __init__: constructor de la clase ArchivoErroresValidacion
	Entradas: la misma clase
	Salidas: ninguna
	"""
	def __init__(self):
		super(ArchivoErroresValidacion, self).__init__('Tipos de datos aceptados: ' +', '.join(ArchivosCampo.extensionesValidas))

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Clase ArchivosCampos: define la clase de los campos disponibles para un formulario de archivos
Entradas: hereda de FileField, ninguna
"""

class ArchivosCampo(forms.FileField):

	contenidosValidos = ('text/html', 'text/plain', 'text/rtf', 'text/xml', 'application/msword', 'application/rtf', 'application/pdf')
	extensionesValidas = ('odt', 'pdf', 'doc', 'txt', 'html', 'rtf', 'htm', 'xhtml')

	"""
	Funcion __init__: constructor de la clase ArchivosCampos
	Entradas: la misma clase
	Salidas: ninguna
	"""
	def __init__(self, contenidosValidos=None, extensionesValidas=None, *args, **kwargs):
		super(ArchivosCampo, self).__init__(*args, **kwargs)
		if contenidosValidos:
			self.contenidosValidos = contenidosValidos
		if extensionesValidas:
			self.extensionesValidas = extensionesValidas

	"""
	Funcion clean: valida los campos tipo ArchivosCampo
	Entradas: la misma clase
	Salidas: ninguna
	"""
	def clean(self, datos, datosIniciales=None):
		archivoActual = super(ArchivosCampo, self).clean(datos, datosIniciales)
		contenidoArchivo = archivoActual.content_type
		extensionActual = splitext(f.name)[1][1:].lower()
		if extensionActual in self.extensionesValidas and contenidoArchivo in self.contenidosValidos:
			return archivoActual
		raise ArchivoErroresValidacion()

# -----------------------------------------------------------------------