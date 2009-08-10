# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/almacenamiento/admin.py
Julian Perez
Ultima modificacion: Mayo 26 de 2009, 09:26
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

from django.contrib import admin
from savia.modulos.almacenamiento.models import Archivo
from savia.modulos.almacenamiento.forms import ArchivoFormulario

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Clase ArchivoAdmin: Define el modelo para administrar los archivos
Entradas: hereda de ModelAdmin, ninguna
"""

class ArchivoAdmin(admin.ModelAdmin):

	# Campos para mostrar de cada instancia
	list_display = ('usuarioAsociado', 'extension', 'nombre', 'archivo', 'fechaCreacion',)
	# Campos que sirven como flitros
	list_filter = ('extension',)
	# Campos que sirven para busqueda
	search_fields = ('usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__email', 'extension', 'nombre',)

# -----------------------------------------------------------------------

# Registrando cada modelo en el sitio de administracion para que sea visible
admin.site.register(Archivo, ArchivoAdmin)

# -----------------------------------------------------------------------