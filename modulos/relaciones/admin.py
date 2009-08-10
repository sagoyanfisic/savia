# coding=latin-1

# --------------------------------------------------
"""
savia/modulos/relaciones/admin.py
Julian Perez
Ultima modificacion: Agosto 01 de 2009, 10:00
"""
# --------------------------------------------------



# --------------------------------------------------
""" Importaciones """

from django.contrib import admin
from savia.modulos.relaciones.models import Mensaje, Amistad, ActividadReciente

# --------------------------------------------------

# --------------------------------------------------
"""
Clase MensajeAdmin: Define el modelo para administrar los mensajes
Entradas: hereda de ModelAdmin, ninguna
"""

class MensajeAdmin(admin.ModelAdmin):

	# Campos para mostrar de cada instancia
   list_display = ('usuarioOrigen', 'titulo', 'usuarioDestino', 'fechaHoraCreacion', 'esImportante', 'esNuevo',)
	# Campos que sirven como flitros
   list_filter = ('esImportante', 'esNuevo',)
	# Campos que sirven para busqueda
   search_fields = ('usuarioOrigen__username', 'usuarioDestino__username', 'titulo',)

# --------------------------------------------------

# --------------------------------------------------
"""
Clase AmistadAdmin: Define el modelo para administrar las amistades
Entradas: hereda de ModelAdmin, ninguna
"""

class AmistadAdmin(admin.ModelAdmin):

	# Campos para mostrar de cada instancia
   list_display = ('usuarioSolicitante', 'usuarioConfirmante', 'fechaHoraSolicitud', 'esSolicitudAprobada', 'fechaHoraAprobacion', 'destacadaSolicitante', 'destacadaConfirmante',)
	# Campos que sirven como flitros
   list_filter = ('esSolicitudAprobada',)
	# Campos que sirven para busqueda
   search_fields = ('usuarioSolicitante__username', 'usuarioConfirmante__username', 'usuarioSolicitante__first_name', 'usuarioConfirmante__first_name', 'usuarioSolicitante__last_name', 'usuarioConfirmante__last_name',)

# --------------------------------------------------

# --------------------------------------------------
"""
Clase ActividadRecienteAdmin: Define el modelo para administrar las actividades recientes
Entradas: hereda de ModelAdmin, ninguna
"""

class ActividadRecienteAdmin(admin.ModelAdmin):

	# Campos para mostrar de cada instancia
   list_display = ('usuarioAsociado', 'fechaHoraRealizacion', 'descripcion', )
	# Campos que sirven como flitros
   list_filter = (  )
	# Campos que sirven para busqueda
   search_fields = ('usuarioAsociado__username', 'usuarioAsociado__first_name', 'usuarioAsociado__last_name', 'descripcion',)

# --------------------------------------------------

# --------------------------------------------------

# Registrando cada modelo en el sitio de administracion para que sea visible
admin.site.register(Mensaje, MensajeAdmin)
admin.site.register(Amistad, AmistadAdmin)
admin.site.register(ActividadReciente, ActividadRecienteAdmin)

# --------------------------------------------------