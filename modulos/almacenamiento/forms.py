# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/almacenamiento/forms.py
Julian Perez
Ultima modificacion: Marzo 31 de 2009, 09:26
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

from django import forms

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Clase ArchivoFormulario: define el formulario para subir un archivo
Entradas: hereda de Form, ninguna
"""

class ArchivoFormulario(forms.Form):

  archivo = forms.FileField(required=True)
  nombre = forms.CharField(required=True)

# -----------------------------------------------------------------------