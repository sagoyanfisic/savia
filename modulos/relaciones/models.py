# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/relaciones/models.py
Julian Perez
Ultima modificacion: Agosto 01 de 2009, 23:36
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import datetime
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase Mensaje: define el modelo de gestion de los mensajes internos del sistema
Entradas: hereda de Model, ninguna
"""

class Mensaje(models.Model):

	# Campos disponibles para el modelo Mensaje
	usuarioOrigen = models.ForeignKey(User, related_name='usuarioOrigen', verbose_name='usuario de origen')
	usuarioDestino = models.ForeignKey(User, related_name='usuarioDestino', verbose_name='usuario de destino')
	fechaHoraCreacion = models.DateTimeField(u'Fecha y hora de creación', default=datetime.datetime.now())
	titulo = models.CharField(u'Título', max_length=77, default='-sin establecer-')
	contenido = models.TextField(u'Contenido', blank=False, null=False)
	esNuevo = models.BooleanField(u'¿Es nuevo?', default=True)
	esImportante = models.BooleanField(u'¿Es importante?', default=False)
	fechaHoraLectura = models.DateTimeField(u'Fecha y hora de lectura', default=datetime.datetime.now())
	disponibleOrigen = models.BooleanField(u'¿Está disponible para el usuario de origen?', default=True)
	disponibleDestino = models.BooleanField(u'¿Está disponible para el usuario de destino?', default=True)

	# Valores meta de la clase Mensaje
	class Meta:
		ordering = [ '-fechaHoraCreacion', 'usuarioOrigen', 'titulo' ]
	
	"""
	Funcion __unicode__: retorna la representacion por defecto de la clase Mensaje
	Entradas: el mismo modelo
	Salidas: string
	"""
	def __unicode__(self):
		return '%s (de %s para %s)' % (self.titulo, self.usuarioOrigen, self.usuarioDestino)

	"""
	Funcion leerMensaje: actualiza el estado del mensaje actual en el momento de lectura
	Entradas: el mismo modelo
	Salidas: ninguna
	"""
	def leerMensaje(self):
		# Si el mensaje es nuevo
		if self.esNuevo:
			# Cambiar el estado del mensaje porque ya fue leido
			self.esNuevo = False
			self.fechaHoraLectura = datetime.datetime.now()

	"""
	Funcion modificarEstado: actualiza el estado del mensaje actual para marcarlo (o desmarcarlo) como importante
	Entradas: el mismo modelo
	Salidas: ninguna
	"""
	def modificarEstado(self):
		# Si el mensaje es importante, quitarle ese estado
		if self.esImportante:
			self.esImportante = False
		# Si no, otorgarselo
		else:
			self.esImportante = True

	"""
	Funcion alternarImportancia: elimina el mensaje actual
	Entradas: el mismo modelo, usuarioActual:objeto
	Salidas: string
	"""
	def eliminarMensaje(self, usuarioActual):
		# Si el usuario que desea eliminar este mensaje es el usuario de origen
		if self.usuarioOrigen==usuarioActual:
			self.disponibleOrigen = False
			# Si el usuario de destino ya elimino el mensaje, se debe eliminar por completo
			if not self.disponibleDestino:
				self.delete()
			else:
				self.save()
			return 'tipoUsuario_origen'
		# Si el usuario que desea eliminar este mensaje es el usuario de destino
		if self.usuarioDestino==usuarioActual:
			self.disponibleDestino = False
			# Si el usuario de origen ya elimino el mensaje, se debe eliminar por completo
			if not self.disponibleOrigen:
				self.delete()			
			else:
				self.save()
			return 'tipoUsuario_destino'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase Amistad: define el modelo de gestion de las amistades
Entradas: hereda de Model, ninguna
"""

class Amistad(models.Model):

	# Campos disponibles para el modelo Amistad
	usuarioSolicitante = models.ForeignKey(User, related_name='usuarioSolicitante', verbose_name='usuario solicitante')
	usuarioConfirmante = models.ForeignKey(User, related_name='usuarioConfirmante', verbose_name='usuario confirmante')
	fechaHoraSolicitud = models.DateTimeField(u'Fecha y hora de la solicitud', default=datetime.datetime.now())
	esSolicitudAprobada = models.BooleanField(u'¿La solicitud fue aprobada?', default=False)
	fechaHoraAprobacion = models.DateTimeField(u'Fecha y hora de la aprobación', default=datetime.datetime.now())
	destacadaSolicitante = models.BooleanField(u'¿Es importante para el usuario solicitante?', default=False)
	destacadaConfirmante = models.BooleanField(u'¿Es importante para el usuario confirmante?', default=False)
	modoAdministrador = models.BooleanField(u'¿Habilitar modo administrador?', default=False)
	
	# Valores meta de la clase Amistad
	class Meta:
		verbose_name_plural = 'Amistades'
		unique_together = (('usuarioSolicitante', 'usuarioConfirmante'),)		
		ordering = [ '-fechaHoraSolicitud', 'usuarioSolicitante', 'usuarioConfirmante' ]
	
	"""
	Funcion __unicode__: retorna la representacion por defecto de la clase Mensaje
	Entradas: el mismo modelo
	Salidas: string
	"""
	def __unicode__(self):
		return '%s - %s' % (self.usuarioSolicitante, self.usuarioConfirmante)

	"""
	Funcion aprobarSolicitud: confirma la amistad actual porque la solicitud fue aprobada
	Entradas: el mismo modelo
	Salidas: ninguna
	"""
	def aprobarSolicitud(self):
		# Aprobando la solicitud de amistad
		self.esSolicitudAprobada = True
		self.fechaHoraAprobacion = datetime.datetime.now()
		# Notificando al usuario solicitante
		usuarioAdministrador = User.objects.get(username=settings.NOMBRE_USUARIO_ADMIN)
		contenidoMensaje = u'Hola. Solo queriamos informarte que ' +self.usuarioConfirmante.username+ ' ha aprobado la solicitud de amistad que le enviaste. Ahora, ' +self.usuarioConfirmante.first_name+ ' y tu son amigos.'
		mensajeNotificacion = Mensaje(usuarioOrigen=usuarioAdministrador, usuarioDestino=self.usuarioSolicitante, titulo='solicitud de amistad aprobada', contenido=contenidoMensaje, esImportante=True, disponibleOrigen=False)
		mensajeNotificacion.save()

	"""
	Funcion modificarEstado_solicitante: actualiza el estado de la amistad actual para marcarla (o desmarcarla) como amistad destacada para el usuario solicitante 
	Entradas: el mismo modelo
	Salidas: ninguna
	"""
	def modificarEstado_solicitante(self):
		# Si ela amistad es destacada, quitarle ese estado
		if self.destacadaSolicitante:
			self.destacadaSolicitante = False
		# Si no, otorgarselo
		else:
			self.destacadaSolicitante = True

	"""
	Funcion modificarEstado_confirmante: actualiza el estado de la amistad actual para marcarla (o desmarcarla) como amistad destacada para el usuario confirmante 
	Entradas: el mismo modelo
	Salidas: ninguna
	"""
	def modificarEstado_confirmante(self):
		# Si ela amistad es destacada, quitarle ese estado
		if self.destacadaConfirmante:
			self.destacadaConfirmante = False
		# Si no, otorgarselo
		else:
			self.destacadaConfirmante = True				
	
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion retornarListaAmigos: retorna la lista de usuarios que tienen vinculo de amistad con el usuario actual
Entradas: usuarioActual:objeto
Salidas: list, boolean
"""

def retornarListaAmigos(usuarioActual):
	try:
		amistadesSolicitadas = Amistad.objects.select_related().filter(usuarioSolicitante=usuarioActual)
		amistadesConfirmadas = Amistad.objects.select_related().filter(usuarioConfirmante=usuarioActual)
		amistadesEstablecidas = (amistadesSolicitadas | amistadesConfirmadas).filter(esSolicitudAprobada=True, modoAdministrador=False).order_by('fechaHoraAprobacion')
		listaUsuariosAdecuados = list()
		for amistadActual in amistadesEstablecidas:
			if amistadActual.usuarioSolicitante == usuarioActual:
				usuarioReferencia = amistadActual.usuarioConfirmante
			if amistadActual.usuarioConfirmante == usuarioActual:
				usuarioReferencia = amistadActual.usuarioSolicitante
			if not usuarioReferencia.is_staff:
				listaUsuarioReferencia = ( usuarioReferencia.id, usuarioReferencia.get_full_name()+ ' --- ' +usuarioReferencia.username )
				listaUsuariosAdecuados.append(listaUsuarioReferencia)
		if len(listaUsuariosAdecuados) == 0:
			operacionExitosa = False
		else:
			operacionExitosa = True
	except:
		listaUsuariosAdecuados = None
		operacionExitosa = False
	return listaUsuariosAdecuados, operacionExitosa

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion sonAmigos: determina si un usuario es amigo del usuario actual
Entradas: usuarioActual:objeto, usuarioReferencia:string
Salidas: boolean
"""

def sonAmigos(usuarioActual, usuarioReferencia):
	if usuarioActual.username == usuarioReferencia:
		return True
	else:
		try:
			amistadSolicitadaActual = Amistad.objects.filter(usuarioSolicitante=usuarioActual, usuarioConfirmante__username=usuarioReferencia, esSolicitudAprobada=True).count()
			amistadSolicitadaReferencia = Amistad.objects.filter(usuarioSolicitante__username=usuarioReferencia, usuarioConfirmante=usuarioActual, esSolicitudAprobada=True).count()
			if (amistadSolicitadaActual+amistadSolicitadaReferencia) > 0:
				return True
			else:
				return False
		except:
			return False

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion existeSolicitudAmistad: determina si entre dos usuarios ya existe una solicitud de amistad pendiente
Entradas: usuarioActual:objeto, usuarioReferencia:string
Salidas: boolean
"""

def existeSolicitudAmistad(usuarioActual, usuarioReferencia):
	try:
		amistadSolicitadaActual = Amistad.objects.filter(usuarioSolicitante=usuarioActual, usuarioConfirmante__username=usuarioReferencia, esSolicitudAprobada=False).count()
		amistadSolicitadaReferencia = Amistad.objects.filter(usuarioSolicitante__username=usuarioReferencia, usuarioConfirmante=usuarioActual, esSolicitudAprobada=False).count()
		if (amistadSolicitadaActual+amistadSolicitadaReferencia) > 0:
			return True
		else:
			return False
	except:
		return False

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion obtenerFechaHoraAmistad: retorna la fecha y la hora de establecimiento de la amistad
Entradas: usuarioActual:objeto, usuarioReferencia:string
Salidas: date
"""

def obtenerFechaHoraAmistad(usuarioActual, usuarioReferencia):
	try:
		amistadSolicitadaActual = Amistad.objects.filter(usuarioSolicitante=usuarioActual, usuarioConfirmante__username=usuarioReferencia, esSolicitudAprobada=True)
		amistadSolicitadaReferencia = Amistad.objects.filter(usuarioSolicitante__username=usuarioReferencia, usuarioConfirmante=usuarioActual, esSolicitudAprobada=True)
		if len(amistadSolicitadaActual) == 1:
			return amistadSolicitadaActual[0].fechaHoraAprobacion
		elif len(amistadSolicitadaReferencia) == 1:
			return amistadSolicitadaReferencia[0].fechaHoraAprobacion
		else:
			return None
	except:
		return None

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase ActividadReciente: define el modelo de gestion de los mensajes internos del sistema
Entradas: hereda de Model, ninguna
"""

class ActividadReciente(models.Model):

	# Campos disponibles para el modelo ActividadReciente
	usuarioAsociado = models.ForeignKey(User, verbose_name='usuario asociado')
	fechaHoraRealizacion = models.DateTimeField(u'Fecha y hora de realización', default=datetime.datetime.now())
	descripcion = models.TextField(u'Descripción', blank=False, null=False)

	# Valores meta de la clase ActividadReciente
	class Meta:
		verbose_name_plural = 'Actividades recientes'
		ordering = [ '-fechaHoraRealizacion', 'usuarioAsociado', 'descripcion' ]
		

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearReporteActividadReciente: crea un reporte de actividad reciente
Entradas: usuarioAsociado:objeto, descripcionActividad:string
Salidas: ninguna
"""

def crearReporteActividadReciente(usuarioAsociado, descripcionActividad):
	actividadReciente = ActividadReciente(usuarioAsociado=usuarioAsociado, descripcion=u'' +descripcionActividad)
	actividadReciente.fechaHoraRealizacion = datetime.datetime.now()
	actividadReciente.save()			

# ----------------------------------------------------------------------