# coding=latin-1

# --------------------------------------------------
"""
savia/modulos/usuarios/admin.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 10:00
"""
# --------------------------------------------------



# --------------------------------------------------
""" Importaciones """

from django.contrib import admin
from savia.modulos.usuarios.models import Perfil, Avatar

# --------------------------------------------------

# --------------------------------------------------
"""
Clase PerfilAdmin: Define el modelo para administrar los perfiles
Entradas: hereda de ModelAdmin, ninguna
"""

class PerfilAdmin(admin.ModelAdmin):

	# Campos para mostrar de cada instancia
	list_display = ('user', 'sexo', 'pais', 'lugar', 'fechaNacimiento', 'url',)
	# Campos que sirven como filtros
	list_filter = ('sexo',)
	# Campos que sirven para busqueda
	search_fields = ('user__username', 'user__first_name', 'user__last_name',)

# --------------------------------------------------

# --------------------------------------------------
"""
Clase AvatarAdmin: Define el modelo para administrar los avatares
Entradas: hereda de ModelAdmin, ninguna
"""

class AvatarAdmin(admin.ModelAdmin):

	# Campos para mostrar de cada instancia
   list_display = ('usuarioAsociado', 'fechaHoraCreacion', 'esValida',)
	# Campos que sirven como flitros
   list_filter = ('esValida',)
	# Campos que sirven para busqueda
   search_fields = ('user__username', 'user__first_name', 'user__last_name',)

# --------------------------------------------------

# --------------------------------------------------

# Registrando cada modelo en el sitio de administracion para que sea visible
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Avatar, AvatarAdmin)

# --------------------------------------------------