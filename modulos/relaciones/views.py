# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/relaciones/views.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 09:51
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.sites.models import RequestSite
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from savia.modulos.relaciones.models import Mensaje, Amistad, ActividadReciente, sonAmigos, obtenerFechaHoraAmistad, crearReporteActividadReciente
from savia.modulos.usuarios.models import Perfil
from savia.modulos.relaciones.forms import EnviarMensajeFormulario, EnviarCorreoFormulario, ResponderMensajeFormulario, BusquedaUsuariosFormulario
from savia.modulos.utilidades.utils import crearImagenDireccionCorreo, calcularEdad

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarMensajes_recibidos: muestra todos los mensajes recibidos
"""

@login_required
def mostrarMensajes_recibidos(peticion):
	usuarioActual = peticion.user
	try:
		mensajesInternos = Mensaje.objects.filter(usuarioDestino=usuarioActual, disponibleDestino=True)
		numeroTotalMensajes = len(mensajesInternos)
	except:
		mensajesInternos = None
		numeroTotalMensajes = 0
	# Creando un objeto que distribuya los los mensajes en paginas (si es necesario)
	paginacionContenido = Paginator(mensajesInternos, settings.NUMERO_OBJETOS_PAGINA)
	try:
		paginaActual = int(peticion.GET['pagina'])
	except:
		paginaActual = 1
	try:
		mensajesSeleccionados = paginacionContenido.page(paginaActual)
	except:
		mensajesSeleccionados = paginacionContenido.page(1)
	# Retornando los datos
	diccionario = { 'mostrarRecibidos' : True, 'mensajesSeleccionados' : mensajesSeleccionados, 'numeroTotalMensajes' : numeroTotalMensajes, }
	return render_to_response('relaciones/mostrarMensajes.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista mostrarMensajes_enviados: muestra todos loe mensajes enviados
"""

@login_required
def mostrarMensajes_enviados(peticion):
	usuarioActual = peticion.user
	try:
		mensajesInternos = Mensaje.objects.filter(usuarioOrigen=usuarioActual, disponibleOrigen=True)
		numeroTotalMensajes = len(mensajesInternos)
	except:
		mensajesInternos = None
		numeroTotalMensajes = 0
	# Creando un objeto que distribuya los los mensajes en paginas (si es necesario)
	paginacionContenido = Paginator(mensajesInternos, settings.NUMERO_OBJETOS_PAGINA)
	try:
		paginaActual = int(peticion.GET['pagina'])
	except:
		paginaActual = 1
	try:
		mensajesSeleccionados = paginacionContenido.page(paginaActual)
	except:
		mensajesSeleccionados = paginacionContenido.page(1)
	# Retornando los datos
	diccionario = { 'mostrarRecibidos' : False, 'mensajesSeleccionados' : mensajesSeleccionados, 'numeroTotalMensajes' : numeroTotalMensajes, }
	return render_to_response('relaciones/mostrarMensajes.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista enviarMensaje: muestra y manipula la plantilla para enviar un mensaje
"""

@login_required
def enviarMensaje(peticion):
	usuarioActual = peticion.user	
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = EnviarMensajeFormulario(usuarioActual, peticion.POST)
		# Si es formulario es correcto
		if formulario.is_valid():
			# Envia el mensaje
			formulario.save()
			return render_to_response('relaciones/enviarMensaje.html', context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		formulario = EnviarMensajeFormulario(usuarioActual)
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, }
	return render_to_response('relaciones/enviarMensaje.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista leerMensaje_recibido: muestra la plantilla con el mensaje elegido
"""

@login_required
def leerMensaje_recibido(peticion, idMensaje):
	usuarioActual = peticion.user
	mensajeActual = get_object_or_404(Mensaje, id=idMensaje, usuarioDestino=usuarioActual, disponibleDestino=True)
	mensajeActual.leerMensaje()
	mensajeActual.save()
	paginaOrigen = peticion.GET['paginaOrigen']
	diccionario = { 'esMensajeRecibido' : True, 'mensajeActual' : mensajeActual, 'paginaOrigenMensaje' : paginaOrigen, }
	return render_to_response('relaciones/leerMensaje.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista responderMensaje: muestra y manipula la plantilla para enviar un mensaje
"""

@login_required
def responderMensaje(peticion, idMensaje):
	usuarioActual = peticion.user
	mensajeActual = get_object_or_404(Mensaje, id=idMensaje, usuarioDestino=usuarioActual, disponibleDestino=True)
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = ResponderMensajeFormulario(mensajeActual, peticion.POST)			
		# Si es formulario es correcto
		if formulario.is_valid():
			# Envia el mensaje, bien sea por correo electronico o por el sistema interno
			formulario.save(esConexionSegura=peticion.is_secure(), sobreescribirDominio=RequestSite(peticion).domain)
			return render_to_response('relaciones/responderMensaje.html', context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		formulario = ResponderMensajeFormulario(mensajeActual)
		errorOperacion = False
	paginaOrigen = peticion.GET['paginaOrigen']
	diccionario = { 'mensajeActual' : mensajeActual, 'formulario' : formulario, 'errorOperacion' : errorOperacion, 'paginaOrigenMensaje' : paginaOrigen, }
	return render_to_response('relaciones/responderMensaje.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista enviarCorreo: muestra y manipula la plantilla para enviar un correo electronico
"""

@login_required
def enviarCorreo(peticion, idMensaje):
	usuarioActual = peticion.user
	# Si el usuario actual es el administrador
	if usuarioActual.is_staff:
		mensajeActual = get_object_or_404(Mensaje, id=idMensaje, usuarioDestino=usuarioActual, disponibleDestino=True)
		# Si hay alguna peticion (formulario con datos) se procesa el formulario
		if peticion.method == 'POST':
			formulario = EnviarCorreoFormulario(peticion.POST)			
			# Si es formulario es correcto
			if formulario.is_valid():
				# Envia el mensaje, bien sea por correo electronico o por el sistema interno
				formulario.save(esConexionSegura=peticion.is_secure(), sobreescribirDominio=RequestSite(peticion).domain)
				return render_to_response('relaciones/enviarCorreo.html', context_instance=RequestContext(peticion))
			# Si el formulario contiene errores
			else:
				errorOperacion = True
		# Si no hay alguna peticion se muestra el formulario
		else:
			formulario = EnviarCorreoFormulario()
			errorOperacion = False
		paginaOrigen = peticion.GET['paginaOrigen']
		diccionario = { 'mensajeActual' : mensajeActual, 'formulario' : formulario, 'errorOperacion' : errorOperacion, 'paginaOrigenMensaje' : paginaOrigen, }
		return render_to_response('relaciones/enviarCorreo.html', diccionario, context_instance=RequestContext(peticion))
	else:
		raise Http404()

# ----------------------------------------------------------------------

# -----------------------------------------------------------------------
"""
Vista leerMensaje_enviado: muestra la plantilla con el mensaje elegido
"""

@login_required
def leerMensaje_enviado(peticion, idMensaje):
	usuarioActual = peticion.user
	mensajeActual = get_object_or_404(Mensaje, id=idMensaje, usuarioOrigen=usuarioActual, disponibleOrigen=True)
	paginaOrigen = peticion.GET['paginaOrigen']
	diccionario = { 'esMensajeRecibido' : False, 'mensajeActual' : mensajeActual, 'paginaOrigenMensaje' : paginaOrigen, }
	return render_to_response('relaciones/leerMensaje.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarMensaje_modificarEstado: cambia el estado de importancia del mensaje elegido
"""

@login_required
def editarMensaje_modificarEstado(peticion, idMensaje):
	if peticion.is_ajax():
		usuarioActual = peticion.user
		mensajeActual = get_object_or_404(Mensaje, id=idMensaje, usuarioDestino=usuarioActual, disponibleDestino=True)
		mensajeActual.modificarEstado()
		mensajeActual.save()
		return HttpResponse('respuestaServidor_exito')
	else:
		raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista eliminarMensaje: elimina el mensaje elegido de acuerdo al usuario actual
"""

@login_required
def eliminarMensaje(peticion, idMensaje):
	mensajeActual = get_object_or_404(Mensaje, id=idMensaje)
	usuarioActual = peticion.user
	tipoUsuario = mensajeActual.eliminarMensaje(usuarioActual)
	paginaOrigen = peticion.GET['paginaOrigen']
	# Seleccionado el redirecionamiento adecuado
	if tipoUsuario == 'tipoUsuario_origen':
		return HttpResponseRedirect(reverse('enlace_mostrarMensajes_enviados')+ '?pagina=' +paginaOrigen)
	if tipoUsuario == 'tipoUsuario_destino':
		return HttpResponseRedirect(reverse('enlace_mostrarMensajes_recibidos')+ '?pagina=' +paginaOrigen)	

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista busquedaUsuarios: muestra y manipula la plantilla para buscar usuarios
"""

@login_required
def busquedaUsuarios(peticion):
	usuarioActual = peticion.user
	# Si hay alguna peticion (formulario con datos) se procesa el formulario
	if peticion.method == 'POST':
		formulario = BusquedaUsuariosFormulario(peticion.POST)
		# Si es formulario es correcto
		if formulario.is_valid():
			# Obteniendo los valores del formulario
			nombreUsuario = peticion.POST['nombreUsuario']
			sexo = peticion.POST['sexo']
			pais = peticion.POST['pais']
			lugar = peticion.POST['lugar']		
			# Construyendo la consulta adecuada segun los criterios de busqueda
			listaCriterios = { 'user__is_staff' : False, 'user__is_active' : True, }
			if not nombreUsuario == '-sin establecer-':
				listaCriterios['user__username__contains'] = nombreUsuario
			if not sexo == 'z':
				listaCriterios['sexo'] = sexo
			if not pais == 'ZZ':
				listaCriterios['pais'] = pais
			if not lugar == '-sin establecer-':
				listaCriterios['lugar__contains'] = lugar
			# Buscando los usuarios adecuados
			listaUsuarios= Perfil.objects.filter(**listaCriterios).exclude(user=usuarioActual).order_by('user__username')			
			diccionario = { 'listaUsuarios' : listaUsuarios, 'numeroResultados' : len(listaUsuarios), }
			return render_to_response('relaciones/busquedaUsuarios.html', diccionario, context_instance=RequestContext(peticion))
		# Si el formulario contiene errores
		else:
			errorOperacion = True
	# Si no hay alguna peticion se muestra el formulario
	else:
		formulario = BusquedaUsuariosFormulario()
		errorOperacion = False
	diccionario = { 'formulario' : formulario, 'errorOperacion' : errorOperacion, }
	return render_to_response('relaciones/busquedaUsuarios.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarPerfilExtendido: muestra el perfil extendido de un usuario
"""

def mostrarPerfilExtendido(peticion, nombreUsuarioAsociado):
	if nombreUsuarioAsociado == settings.NOMBRE_USUARIO_ADMIN:
		return HttpResponseRedirect(reverse('enlace_mostrarAcercade'))
	else:
		usuarioActual = peticion.user
		# Esta seccion es solo valida para usuarios que son amigos entre si
		if sonAmigos(usuarioActual, nombreUsuarioAsociado):
			perfilExtendido = get_object_or_404(User, username=nombreUsuarioAsociado, is_active=True).get_profile()
			rutaImagenDireccionCorreo = crearImagenDireccionCorreo(perfilExtendido.user)
			fechaHoraAmistad = obtenerFechaHoraAmistad(usuarioActual, nombreUsuarioAsociado)
			actividadesRecientes = ActividadReciente.objects.filter(usuarioAsociado__username=nombreUsuarioAsociado).order_by('-fechaHoraRealizacion')[:13]
			diccionario = {
				'perfilExtendido' : perfilExtendido,
				'llaveGoogleMaps': settings.LLAVE_GOOGLEMAPS,
				'rutaImagenDireccionCorreo' : rutaImagenDireccionCorreo,
				'fechaHoraAmistad': fechaHoraAmistad,
				'numeroActividadesRecientes' : len(actividadesRecientes),
				'actividadesRecientes' : actividadesRecientes,
			}
			return render_to_response('relaciones/mostrarPerfilExtendido.html', diccionario, context_instance=RequestContext(peticion))
		else:
			raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista enviarSolicitudAmistad: envia una solicitud de amistad al usuario solicitado
"""

@login_required
def enviarSolicitudAmistad(peticion, nombreUsuarioSolicitado):
	if peticion.is_ajax():
		usuarioActual = peticion.user
		# Si los dos usuarios ya son amigos
		if sonAmigos(usuarioActual, nombreUsuarioSolicitado):
			raise Http404()
		else:
			usuarioSolicitado = User.objects.get(username=nombreUsuarioSolicitado)
			solicitarAmistad = Amistad(usuarioSolicitante=usuarioActual, usuarioConfirmante=usuarioSolicitado, esSolicitudAprobada=False, modoAdministrador=False)
			solicitarAmistad.save()		
			return HttpResponse('respuestaServidor_exito')
	else:
		raise Http404()			

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarSolicitudesAmistad: muestra todas las amistades establecidas
"""

@login_required
def mostrarSolicitudesAmistad(peticion):
	usuarioActual = peticion.user
	try:
		solicitudesAmistad = Amistad.objects.filter(usuarioConfirmante=usuarioActual, esSolicitudAprobada=False, modoAdministrador=False).order_by('-fechaHoraSolicitud')
		numeroTotalSolicitudes = len(solicitudesAmistad)
	except:
		amistadesEstablecidas = None
		numeroTotalAmistades = 0
	# Creando un objeto que distribuya los los mensajes en paginas (si es necesario)
	paginacionContenido = Paginator(solicitudesAmistad, settings.NUMERO_OBJETOS_PAGINA)
	try:
		paginaActual = int(peticion.GET['pagina'])
	except:
		paginaActual = 1
	try:
		solicitudesSeleccionadas = paginacionContenido.page(paginaActual)
	except:
		solicitudesSeleccionadas = paginacionContenido.page(1)
	# Retornando los datos
	diccionario = { 'solicitudesSeleccionadas' : solicitudesSeleccionadas, 'numeroTotalSolicitudes' : numeroTotalSolicitudes, }
	return render_to_response('relaciones/mostrarSolicitudesAmistad.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarSolicitudAmistad_aprobar: aprueba la solicitud de amistad actual
"""

@login_required
def editarSolicitudAmistad_aprobar(peticion, idSolicitud):
	amistadActual = get_object_or_404(Amistad, id=idSolicitud)
	amistadActual.aprobarSolicitud()
	amistadActual.save()
	# Reportando la actividad reciente
	crearReporteActividadReciente(amistadActual.usuarioConfirmante, u' y ' +amistadActual.usuarioSolicitante.username+ ' ahora son amigos')
	crearReporteActividadReciente(amistadActual.usuarioSolicitante, u' y ' +amistadActual.usuarioConfirmante.username+ ' ahora son amigos')
	paginaOrigen = peticion.GET['paginaOrigen']
	return HttpResponseRedirect(reverse('enlace_mostrarSolicitudesAmistad')+ '?pagina=' +paginaOrigen)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarSolicitudAmistad_rechazar: rechaza la solicitud de amistad actual
"""

@login_required
def editarSolicitudAmistad_rechazar(peticion, idSolicitud):
	amistadActual = get_object_or_404(Amistad, id=idSolicitud)
	amistadActual.delete()
	paginaOrigen = peticion.GET['paginaOrigen']
	return HttpResponseRedirect(reverse('enlace_mostrarSolicitudesAmistad')+ '?pagina=' +paginaOrigen)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista mostrarListaAmigos: muestra todas las amistades establecidas
"""

@login_required
def mostrarListaAmigos(peticion):
	usuarioActual = peticion.user
	try:
		amistadesSolicitadas = Amistad.objects.filter(usuarioSolicitante=usuarioActual)
		amistadesConfirmadas = Amistad.objects.filter(usuarioConfirmante=usuarioActual)
		amistadesEstablecidas = (amistadesSolicitadas | amistadesConfirmadas).filter(esSolicitudAprobada=True, modoAdministrador=False).order_by('-fechaHoraAprobacion')
		numeroTotalAmistades = len(amistadesEstablecidas)
	except:
		amistadesEstablecidas = None
		numeroTotalAmistades = 0
	# Creando un objeto que distribuya los los mensajes en paginas (si es necesario)
	paginacionContenido = Paginator(amistadesEstablecidas, settings.NUMERO_OBJETOS_PAGINA)
	try:
		paginaActual = int(peticion.GET['pagina'])
	except:
		paginaActual = 1
	try:
		amistadesSeleccionadas = paginacionContenido.page(paginaActual)
	except:
		amistadesSeleccionadas = paginacionContenido.page(1)
	# Retornando los datos
	diccionario = { 'amistadesSeleccionadas' : amistadesSeleccionadas, 'numeroTotalAmistades' : numeroTotalAmistades, }
	return render_to_response('relaciones/mostrarListaAmigos.html', diccionario, context_instance=RequestContext(peticion))

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista editarAmistad_modificarEstado: cambia el estado de la amistad segun el usuario actual y si es destacada o no
"""

@login_required
def editarAmistad_modificarEstado(peticion, idAmistad):
	if peticion.is_ajax():
		usuarioActual = peticion.user
		amistadActual = get_object_or_404(Amistad, id=idAmistad, modoAdministrador=False)
		if amistadActual.usuarioSolicitante == usuarioActual:
			amistadActual.modificarEstado_solicitante()
		if amistadActual.usuarioConfirmante == usuarioActual:
			amistadActual.modificarEstado_confirmante()
		amistadActual.save()
		return HttpResponse('respuestaServidor_exito')
	else:
		raise Http404()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Vista eliminarAmistad: elimina la amistad elegida de manera unilateral e irreversible
"""

@login_required
def eliminarAmistad(peticion, idAmistad):
	amistadActual = get_object_or_404(Amistad, id=idAmistad)
	amistadActual.delete()
	paginaOrigen = peticion.GET['paginaOrigen']
	return HttpResponseRedirect(reverse('enlace_mostrarListaAmigos')+ '?pagina=' +paginaOrigen)

# ----------------------------------------------------------------------