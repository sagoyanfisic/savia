# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/almacenamiento/models.py
Julian Perez
Ultima modificacion: Mayo 26 de 2009, 09:26
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

import os
import os.path
import datetime
from django.conf import settings
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.files.uploadhandler import MemoryFileUploadHandler, FileUploadHandler, UploadFileException

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Funcion destinoArchivos: determina la ruta adecuada para almacenar un archivo
Entradas: el mismo modelo
Salidas: string
"""

def destinoArchivos(instancia, nombreArchivo):
	return settings.DESTINO_ARCHIVOS+ '/%s/%s' % (instancia.usuarioAsociado.username, nombreArchivo)

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Clase Archivo: define el modelo de un archivo de un usuario
Entradas: hereda de Model, ninguna
"""

class Archivo(models.Model):

	usuarioAsociado = models.ForeignKey(User, verbose_name="usuario asociado")
	fechaCreacion = models.DateTimeField(u'Fecha y hora de creación', default=datetime.datetime.now)
	archivo = models.FileField(upload_to=destinoArchivos)
	extension = models.CharField(u"Extensión", max_length=80)
	nombre = models.CharField(u"Nombre del archivo", max_length=80)

	"""
	Funcion __unicode__: retorna la representacion por defecto de una instancia de la clase Archivo
	Entradas: el mismo modelo
	Salidas: string
	"""
	def __unicode__(self):
		return "%s: %s.%s" % (self.usuarioAsociado, self.nombre, self.extension)

# -----------------------------------------------------------------------
"""
Clase ArchivoProgreso: define el modelo del progreso de un archivo
Entradas: hereda de FileUploadHandler, ninguna
"""

class ArchivoProgreso(FileUploadHandler):

	"""
	Funcion __init__: constructor de la clase ArchivoProgreso
	Entradas: la misma clase
	Salidas: ninguna
	"""
	def __init__(self, peticion=None, rutaSalida="/tmp"):
		super(ArchivoProgreso, self).__init__(peticion)
		self.idProgreso = None
		self.llaveCache = None
		self.peticion = peticion
		self.rutaSalida = rutaSalida
		self.destinoSubida = None

	"""
	Funcion manipularEntrada: manipula el archivo de entrada
	Entradas: la misma clase, datosEntrada:object, datosMeta:diccionario, longitudContenido:int, limitesContenido:int, codificacion:string
	Salidas: ninguna
	"""
	def manipularEntrada(self, datosEntrada, datosMeta, longitudContenido, limitesContenido, codificacion=None):
		self.longitudContenido = longitudContenido
		if 'ArchivoProgreso-ID' in self.peticion.GET:
			self.idProgreso = self.peticion.GET['ArchivoProgreso-ID']
		elif 'ArchivoProgreso-ID' in self.peticion.META:
			self.idProgreso = self.peticion.META['ArchivoProgreso-ID']
		if self.idProgreso:
			self.llaveCache = self.progress_id
			self.peticion.session['archivoProgreso_%s' % self.llaveCache] = { 'longitudTotal': self.longitudContenido, 'longitudActual' : 0, }

	"""
	Funcion nuevoArchivo: crea un nuevo archivo para subir
	Entradas: la misma clase, nombreCampo:string, nombreArchivo:string, contenidoArchivo:string, longitudContenido:int, caracteres:string
	Salidas: ninguna
	"""
	def nuevoArchivo(self, nombreCampo, nombreArchivo, contenidoArchivo, longitudContenido, caracteres=None):
		self.rutaSalida = os.path.join(self.rutaSalida, nombreArchivo)
		self.destinoSubida = open(self.nuevoArchivo, 'wb+')
		pass

	"""
	Funcion recibirDatos: recibe los datos en trozos y actualiza el progreso
	Entradas: la misma clase, nombreCampo:string, nombreArchivo:string, contenidoArchivo:string, longitudContenido:int, caracteres:string
	Salidas: ninguna
	"""
	def recibirDatos(self, datosArchivo, inicioArchivo):
		datosActuales = self.peticion.session['archivoProgreso_%s' % self.llaveCache]
		datosActuales['progresoActual'] += self.chunk_size
		self.peticion.session['archivoProgreso_%s' % self.llaveCache] = data
		self.peticion.session.save()
		self.destinoSubida.write(datosArchivo)
		return None

	"""
	Funcion archivoCompleto: cuando el archivo se completa
	Entradas: la misma clase, tamanoArchivo:int
	Salidas: ninguna
	"""
	def archivoCompleto(self, tamanoArchivo):
		pass

	"""
	Funcion subidaCompleta: termina la subida del archivo y del seguimiento del progreso
	Entradas: la misma clase
	Salidas: ninguna
	"""
	def subidaCompleta(self):
		try:
			self.destinoSubida.close()
		except:
			pass
		del self.peticion.session['archivoProgreso_%s' % self.llaveCache]

# -----------------------------------------------------------------------