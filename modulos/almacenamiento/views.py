# coding=latin-1

# -----------------------------------------------------------------------
"""
savia/modulos/almacenamiento/views.py
Eduardo Aragón Montes
Ultima modificacion: Mayo 26 de 2009, 19:30
"""
# -----------------------------------------------------------------------



# -----------------------------------------------------------------------
""" Importaciones """

import os
import os.path
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, Http404
from savia.modulos.almacenamiento.models import Archivo, ArchivoProgreso
from savia.modulos.almacenamiento.forms import ArchivoFormulario

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarEspacio: muestra el espacio de un usuario
"""

@login_required
def mostrarEspacio(peticion):
	listaArchivos = Archivo.objects.filter(usuarioAsociado=peticion.user)
	diccionario = { 'listaArchivos': listaArchivos, }
	return render_to_response('almacenamiento/mostrarEspacio.html', diccionario, context_instance=RequestContext(peticion))

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarInicio: muestra y manipula el formulario de subida de un archivo
"""

@login_required
def subirArchivo(peticion):
	if peticion.method == 'POST':
		formulario = ArchivoFormulario(peticion.POST, peticion.FILES)
		if formulario.is_valid():
			archivoSubido = formulario.cleaned_data.get('archivo')
			nombreOriginalArchivo = str(archivoSubido)
			nombreAsignadoArchivo = formulario.cleaned_data.get('nombre')
			# Asignadole el nombre personalizado al archivo subido
			nombre, extensionArchivo = os.path.splitext(nombreOriginalArchivo)
			nuevoArchivo = Archivo(usuarioAsociado=peticion.user, archivo=archivoSubido, nombre=nombreAsignadoArchivo, extension=extensionArchivo.strip("."))
			#nuevoArchivo.archivo.save('%s%s' % (nombreAsignadoArchivo, extensionArchivo), archivoSubido)
			#nuevoArchivo.save()
	else:
		formulario = ArchivoFormulario()
		nombreAsignadoArchivo = ''
		extensionArchivo = ''
		nombreOriginalArchivo = ''
	diccionario = { 'formulario' : formulario, 'nombreAsignadoArchivo' : nombreAsignadoArchivo+extensionArchivo, 'nombreOriginalArchivo' : nombreOriginalArchivo, }
	return render_to_response('almacenamiento/subirArchivo.html', diccionario, context_instance=RequestContext(peticion))

# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista subirArchivo_progreso: muestra el progreso actual de la subida del archivo
"""

def subirArchivo_progreso(peticion):
	idProgreso = ''
	if 'ArchivoProgreso-ID' in peticion.GET:
		idProgreso = request.GET['ArchivoProgreso-ID']
	elif 'ArchivoProgreso-ID' in peticion.META:
		idProgreso = request.META['ArchivoProgreso-ID']
	if idProgreso:
		llaveCache = '%s' % (idProgreso)
		datos = peticion.session.get('archivoProgreso_%s' % llaveCache, None)
		return HttpResponse(simplejson.dumps(datos))
	else:
		return HttpResponse('respuestaServidor_error')

# view thath launch the upload process
def upload_form(request):
	if request.method == 'POST':
		outPath = os.path.join(settings.DESTINO_ARCHIVOS, str(request.user.id))   # set your upload path here
		if not os.path.exists(outPath):
			os.makedirs(outPath)
		request.upload_handlers.insert(0, ProgressUploadHandler(request, outPath)) # place our custom upload in first position
		upload_file = request.FILES.get('file', None)   # start the upload
		return HttpResponse("uploaded ok")
	else:
		return render_to_response('archivos/subir_exito.html', context_instance=RequestContext(request))

# -----------------------------------------------------------------------