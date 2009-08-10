# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/utilidades/etiquetas.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 18:13
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import re
import os
import time
import datetime
import Image
from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from django.template import Library, Node, Template, TemplateSyntaxError, Variable
from savia.modulos.usuarios.models import Perfil, Avatar
from savia.modulos.relaciones.models import sonAmigos, existeSolicitudAmistad

# ----------------------------------------------------------------------
""" Variables globales para este archivo """

# Creando el objeto tipo Library para registrar y utlizar en las plantillas las etiquetas personalizadas
register = template.Library()
BOTON_ACEPTAR = """<a class="a_enlacePequeno" title="ocultar este mensaje | """ +settings.NOMBRE_APLICACION+ """" href="/" onClick="return mostrarOcultarElemento('p_mensajeEstado');">(aceptar)</a>"""

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarEnlace: verificar si JavaScript esta habilitado desde el lado del cliente
Entradas: ninguna
Salidas: string
"""

def verificarJavascript():
	verificarJavascript = """
	<p class="p_mensajeEstado error">
	<span class="div_iconoEstado error">&nbsp;&nbsp;&nbsp;</span><span class="span_espacioHorizontal"></span>
	<span class="span_textoResaltado">&iexcl;Ooops! Hay alg&uacute;n error con JavaScript.</span>
	<script type='text/javascript'>
		establecerInterfaz();
		habilitarIndicadorAjax();
	</script>
	<noscript>
	<br/><br/>
	<span class="span_textoResaltado">JavaScript est&aacute; <u>deshabilitado</u>.</span><br/>
	Habilita el uso de JavaScript en las <i>opciones</i> tu navegador e intenta acceder de nuevo.<br/>
	Si JavaScript ya est&aacute; habilitado y a&uacute;n as&iacute; ves este mensaje, <i>actualiza o cambia</i> tu navegador.
	</noscript>
	</p>
	"""
	return verificarJavascript
register.simple_tag(verificarJavascript)

# ----------------------------------------------------------------------
"""
Funcion crearEnlace: retorna la URL de una vista especifica
Entradas: destino:string, argumentos:string, id:string, clase:string, titulo:string, textoEnlace:string
Salidas: string
"""

def crearEnlace(destino, argumentos, identificador, clase, titulo, textoEnlace):
	rutaDestino = destino
	if re.search('enlace_', destino):
		if argumentos=='':
			rutaDestino = reverse(destino)
		else:
			rutaDestino = reverse(destino, args=[argumentos])
	if identificador != '':
		identificador = ' id="' +identificador+ '"'
	if clase != '':
		clase = ' class="' +clase+ '"'		
	if titulo == '':
		titulo = 'enlace'
	return '<a' +identificador+ ''+clase+ ' title="' +titulo+ ' | ' +settings.NOMBRE_APLICACION+ '" href="' +rutaDestino+ '">' +textoEnlace+ '</a>'
register.simple_tag(crearEnlace)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearEnlaceImagen: crea un enlace a una URL utilizando una imagen
Entradas: destino:string, argumentos:string, identificador:string, clase:string, titulo:string, archivoImagen:string, idImagen:string, claseImagen:string
Salidas: string
"""

def crearEnlaceImagen(destino, argumentos, identificador, clase, titulo, archivoImagen, idImagen, claseImagen):
	rutaDestino = destino
	if re.search('enlace_', destino):
		if argumentos=='':
			rutaDestino = reverse(destino)
		else:
			rutaDestino = reverse(destino, args=[argumentos])
	if identificador != '':
		identificador = ' id="' +identificador+ '"'
	if clase != '':
		clase = ' class="' +clase+ '"'		
	if titulo == '':
		titulo = 'enlace'
	if idImagen != '':
		idImagen = ' id="' +idImagen+ '"'
	if claseImagen != '':
		claseImagen = ' class="' +claseImagen+ '"'		
	return '<a' +identificador+ '' +clase+ ' title="' +titulo+ ' | ' +settings.NOMBRE_APLICACION+ '" href="' +rutaDestino+ '"><img' +idImagen+ '' +claseImagen+ ' src="' +settings.URL_IMG+archivoImagen+ '"/></a>'
register.simple_tag(crearEnlaceImagen)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearEnlaceInicio: retornar un enlace para ir a la pagina de inicio
Entradas: textoEnlace:String, enlaceActual:string
Salidas: string
"""

def crearEnlaceInicio(textoEnlace, enlaceSeccion):
	enlaceActual = ''
	if enlaceSeccion:
		enlaceActual = 'class="a_enlaceSeccion actual"'
	return '<a '+enlaceActual+ ' title="inicio | ' +settings.NOMBRE_APLICACION+ '" href="' +reverse('enlace_mostrarInicio')+ '">' +textoEnlace+ '</a>'
register.simple_tag(crearEnlaceInicio)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearEnlaceInicio: retornar un enlace para ir a la pagina de inicio
Entradas: ninguna
Salidas: string
"""

def crearEnlaceContacto():
	return '&iquest;Crees que hay un error? Contacta al <a title="contacto | ' +settings.NOMBRE_APLICACION+ '" href="' +reverse('enlace_mostrarContacto')+ '">administrador</a> y reporta esta situaci&oacute;n.'
register.simple_tag(crearEnlaceContacto)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarCSS: retorna etiquetas tipo 'link' para cargar un archivo CSS
Entradas: ninguna
Salidas: string
"""

def cargarFavicon():
	return '<link rel="shortcut icon" href="' +settings.URL_IMG+ 'savia_favicon.ico">'
register.simple_tag(cargarFavicon)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarCSSBase: retorna etiquetas tipo 'link' para cargar un archivo CSS
Entradas: temaSeleccionado:string
Salidas: string
"""

def cargarCSSBase(usuarioActual):
	try:
		perfilActual = Perfil.objects.get(user=usuarioActual)
		temaActual = perfilActual.temaPreferido
	except:
		temaActual = '808000';
	cargarCSSBase = """
	<link rel="stylesheet" href=\"""" +settings.URL_CSS+ """temas/base_""" +temaActual+ """.css" type="text/css" />
	"""
	return cargarCSSBase
register.simple_tag(cargarCSSBase)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarCSS: retorna etiquetas tipo 'link' para cargar un archivo CSS
Entradas: archivoCSS:string
Salidas: string
"""

def cargarCSS(archivoCSS):
	cargarCSS = """
	<link rel="stylesheet" href=\"""" +settings.URL_CSS+archivoCSS+ """.css" type="text/css" />
	"""
	return cargarCSS
register.simple_tag(cargarCSS)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarJavascript: retorna etiquetas tipo 'link' para cargar un archivo CSS
Entradas: archivoJS:string
Salidas: string
"""

def cargarJavascript(archivoJS):
	cargarJavascript = """
	<script language="JavaScript" type="text/javascript" charset="ISO-8859-1" src=\"""" +settings.URL_JS+archivoJS+ """.js"></script>
	"""
	return cargarJavascript
register.simple_tag(cargarJavascript)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarJavascriptExterno: retorna etiquetas tipo 'link' para cargar un archivo CSS
Entradas: url:string
Salidas: string
"""

def cargarJavascriptExterno(url):
	cargarJavascriptExterno = """
	<script language="JavaScript" type="text/javascript" charset="ISO-8859-1" src=\"""" +url+ """.js"></script>
	"""
	return cargarJavascriptExterno
register.simple_tag(cargarJavascriptExterno)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarFuncionJS: retorna etiquetas tipo 'script' para introducir codigo de Javascript
Entradas: funcionJS:string
Salidas: string
"""

def cargarFuncionJS(funcionJS, parametros):
	# Revisando la lista de parametros
	if parametros:
		listaParametros = str(parametros).split(",")
	else:
		listaParametros = list()
	parametrosFuncionJS = ""
	numeroParametros = len(listaParametros)
	for idx in range(numeroParametros):
		parametrosFuncionJS += "'" +str(listaParametros[idx])+ "'"
		if idx < numeroParametros-1:
			parametrosFuncionJS += ","
	script = """
	<script type='text/javascript'>
		$(window).load(function ()
		{
		""" +funcionJS+ """(""" +parametrosFuncionJS+ """)
		});
	</script>
	"""
	return script
register.simple_tag(cargarFuncionJS)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarLogo: retorna una etiqueta tipo 'img' para cargar el logo
Entradas: ninguna
Salidas: string
"""

def cargarLogo():
	parteIzquierda =  '<img title="sabia savia por mi cuerpo | ' +settings.NOMBRE_APLICACION+ '" src="' +settings.URL_IMG+ 'savia_logo_izq.gif" style="float: left;"/>'
	parteDerecha =  '<img title="sabia savia por mi cuerpo | ' +settings.NOMBRE_APLICACION+ '" src="' +settings.URL_IMG+ 'savia_logo_der.gif" style="float: right;"/>'
	return parteIzquierda+parteDerecha+ '<div style="clear: both;"></div>'
register.simple_tag(cargarLogo)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarImagen: retorna una etiqueta tipo 'img' para cargar una imagen
Entradas: archivoImagen:string, identificador:string, clase:string,  alternativo:string, titulo:string
Salidas: string
"""

def cargarImagen(archivoImagen, identificador, clase, alternativo, titulo):
	if archivoImagen == 'logo':
		archivoImagen = settings.NOMBRE_LOGO
	if alternativo == '':
		alternativo = 'imagen'
	if titulo == '':
		titulo = 'imagen'		
	return '<img id="' +str(identificador)+ '" class="' +clase+ '" title="' +titulo+ ' | ' +settings.NOMBRE_APLICACION+ '" alt="' +alternativo+ ' | ' +settings.NOMBRE_APLICACION+ '" src="' +settings.URL_IMG+archivoImagen+ '"/>'
register.simple_tag(cargarImagen)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion paginaActiva: resaltar un enlace segun corresponda a una seccion
Entradas: peticion:objeto(), patron:string
Salidas: string
"""

def paginaActiva(peticion, patron):
	# Busca el patron en la URL objetivo utilizando expresiones regulares
	if re.search(patron, peticion.path):
		# Retorna 'actual' para indicar que se debe resaltar el enlace
		return 'actual'
	return ''
register.simple_tag(paginaActiva)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearMensajeEstado: retorna un mensaje de error con el mensaje especificado
Entradas: tipoMensaje:string, textoMensaje:string, botonesMensaje:string
Salidas: string
"""

def crearMensajeEstado(tipoMensaje, textoMensaje, botonesMensaje):
	if botonesMensaje == 'aceptar':
		botonesMensaje = '<br/>' +BOTON_ACEPTAR
	textoMensaje = str(textoMensaje)
	return """
	<p class="p_mensajeEstado """ +tipoMensaje+ """">
	<span class="div_iconoEstado """ +tipoMensaje+ """">&nbsp;&nbsp;&nbsp;</span>
	<span class="span_espacioHorizontal"></span>""" +textoMensaje+botonesMensaje+	"""
	</p>"""
register.simple_tag(crearMensajeEstado)

def crearMensajeEstadoExito(textoMensaje):
	textoMensaje = str(textoMensaje)
	return crearMensajeEstado('exito', textoMensaje, '')
register.simple_tag(crearMensajeEstadoExito)

def crearMensajeEstadoError(textoMensaje):
	textoMensaje = str(textoMensaje)
	return crearMensajeEstado('error', textoMensaje, '')
register.simple_tag(crearMensajeEstadoError)

def crearMensajeEstadoAlerta(textoMensaje):
	textoMensaje = str(textoMensaje)
	return crearMensajeEstado('alerta', textoMensaje, '')
register.simple_tag(crearMensajeEstadoAlerta)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearMensajeLineal: retorna un mensaje de error con el mensaje especificado en modo lineal
Entradas: tipoMensaje:string, textoMensaje:string
Salidas: string
"""

def crearMensajeLineal(tipoMensaje, textoMensaje):
	textoMensaje = str(textoMensaje)
	return """<span class="div_iconoEstado """ +tipoMensaje+ """">&nbsp;&nbsp;&nbsp;</span><span class="p_mensajeEstadoLineal """ +tipoMensaje+ """">""" +textoMensaje+ """</span>"""
register.simple_tag(crearMensajeLineal)

def crearMensajeLinealExito(textoMensaje):
	textoMensaje = str(textoMensaje)
	return crearMensajeLineal('exito', textoMensaje)
register.simple_tag(crearMensajeLinealExito)

def crearMensajeLinealError(textoMensaje):
	textoMensaje = str(textoMensaje)
	return crearMensajeLineal('error', textoMensaje)
register.simple_tag(crearMensajeLinealError)

def crearMensajeLinealAlerta(textoMensaje):
	textoMensaje = str(textoMensaje)
	return crearMensajeLineal('alerta', textoMensaje)
register.simple_tag(crearMensajeLinealAlerta)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion mostrarFechaHoraContextual: retorna una cadena de texto de la fecha y la hora actual en forma contextual
Entradas: fechaHoraObjetivo:objeto
Salidas: string
"""

def mostrarFechaHoraContextual(fechaHoraObjetivo):
	# Calcula la diferencia entre fecha y la hora objetivo, y la fecha y la hora actual
	diferenciaTotal = datetime.datetime.today() - fechaHoraObjetivo
	# Calcula la hora referencia del dia
	horaReferencia = fechaHoraObjetivo.hour
	if horaReferencia in range(0,5):
		horaContextual = 'en la madrugada'
	elif horaReferencia in range(5,12):
		horaContextual = 'en la ma&ntilde;ana'
	elif horaReferencia in range(12,14):
		horaContextual = 'al mediod&iacute;a'
	elif horaReferencia in range(14,18):
		horaContextual = 'en la tarde'
	elif horaReferencia in range(18,24):
		horaContextual = 'en la noche'	
	# Calcula los dias y minutos (si es necesario) de diferencia
	semanasDiferencia, diasDiferencia = divmod(diferenciaTotal.days, 7)
	minutosDiferencia, segundosDiferencia = divmod(diferenciaTotal.seconds, 60)
	horasDiferencia, minutosDiferencia = divmod(minutosDiferencia, 60)
	if semanasDiferencia in range(0,1):
		if diasDiferencia in range(0,1):
			if horasDiferencia in range(0,1):	
				if minutosDiferencia in range(0,3):
					fechaContextual = 'hace unos instantes'	
				elif minutosDiferencia in range(3,23):
					fechaContextual = 'hace unos minutos'
				elif minutosDiferencia in range(23,33):
					fechaContextual = 'hace como media hora'
				else:
					fechaContextual = 'hace como una hora'		
			elif horasDiferencia in range(1,3):
				fechaContextual = 'hace un par de horas'
			else:
				if (datetime.datetime.today().hour-horasDiferencia) > 0:
					fechaContextual = 'hoy ' +horaContextual
				else:
					fechaContextual = 'ayer ' +horaContextual					
		elif diasDiferencia in range(1,2):
			if (datetime.datetime.today().hour-horasDiferencia) > 0:
				fechaContextual = 'ayer ' +horaContextual
			else:
				fechaContextual = 'anteayer ' +horaContextual			
		elif diasDiferencia in range(2,3):
			fechaContextual = 'hace unos d&iacute;as ' +horaContextual			
		else:
			fechaContextual = 'esta misma semana '					
	elif semanasDiferencia in range(1,2):
		fechaContextual = 'la semana pasada '
	elif semanasDiferencia in range(2,3):
		fechaContextual = 'hace unos 15 d&iacute;as '
	elif semanasDiferencia in range(3,5):
		fechaContextual = 'hace como un mes'
	elif semanasDiferencia in range(5,9):
		fechaContextual = 'el mes pasado'
	elif semanasDiferencia in range(9,21):
		fechaContextual = 'hace unos meses'
	else:
		fechaContextual = 'hace bastante tiempo'
	# Retorna la cadena de texto con la descripcion contextual de la fecha y la hora
	return fechaContextual
register.simple_tag(mostrarFechaHoraContextual)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion mostrarAvatar: retorna el avatar adecuado para el usuario actual
Entradas: usuarioAsociado:objeto, identificador:string, tituloAlternativo:string
Salidas: string
"""

def mostrarAvatar(usuarioAsociado, identificador, tituloAlternativo):
	urlAvatarActual = ''
	try:
		avatarUsuario = Avatar.objects.get(usuarioAsociado=usuarioAsociado, esValida=True).imagen or None
	except:
		avatarUsuario = None
	if avatarUsuario != None:
		rutaAvatar = avatarUsuario.path
		if os.path.isfile(rutaAvatar):
			rutaAvatar = avatarUsuario.path
			base, filename = os.path.split(rutaAvatar)
			name, extension = os.path.splitext(filename)
			filename = os.path.join(base, '%s%s' % (name, extension))
			base, temp = os.path.split(avatarUsuario.url)
			urlAvatarActual = base+ '/%s%s' % (name, extension)	
	rutaAvatar = settings.RUTA_AVATAR_GENERICO
	base, filename = os.path.split(rutaAvatar)
	name, extension = os.path.splitext(filename)
	generic, extension = os.path.splitext(filename)
	filename = os.path.join(base, '%s%s' % (name, extension))
	urlAvatarGenerico = settings.URL_IMG+ '%s%s' % (generic, extension)
	# Determinado que avatar sera enlazado
	if urlAvatarActual != '':
		urlFinal = urlAvatarActual
	else:
		urlFinal = urlAvatarGenerico
	return """
	<img id=\"""" +identificador+ """"
	alt=\"""" +tituloAlternativo+ """ | """ +settings.NOMBRE_APLICACION+ """" title=\"""" +tituloAlternativo+ """ | """ +settings.NOMBRE_APLICACION+ """"
	src=\"""" +urlFinal+ """"/>"""
register.simple_tag(mostrarAvatar)	

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion mostrarCalendario: retorna un script para la creacion de un calendario y lo asocia a dos campos (uno para la fecha en formato texto y otro en formato fecha)
Entradas: campoObjetivo:string
Salidas: string
"""

def mostrarCalendario(campoObjetivo):
	mostrarCalendario = """
	<script language="JavaScript" type="text/javascript" charset="ISO-8859-1">
		$(function()
		{
			$('#""" +campoObjetivo+ """').datepicker(
			{
				showButtonPanel: true,
				defaultDate: '',
				dateFormat: 'yy-mm-dd',
				changeMonth: true,
				changeYear: true,
				yearRange: '-77:+0',
				altField: '#""" +campoObjetivo+ """Texto',
				altFormat: "DD d \'de\' MM \'de\' yy",
				showOn: 'button',
				buttonImage: '""" +settings.URL_IMG+ """misc_calendario.gif',
				buttonText: 'mostrar/ocultar el calendario | """ +settings.NOMBRE_APLICACION+ """',
				buttonImageOnly: true,
				nextText: 'mes siguiente',
				prevText: 'mes anterior',
				currentText: 'hoy',
				closeText: 'cerrar',
				monthNames: ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Deciembre'],
				monthNamesShort: ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'],
				dayNames: ['Domingo', 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado'],
				dayNamesMin: ['D','L','M','M','J','V','S']
			});
		});
	</script>
	"""
	return mostrarCalendario
register.simple_tag(mostrarCalendario)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion cargarMapa: retorna el script necesario para utilizar los mapas de Google Maps
Entradas: divObjetivo:string, latitud:string, longitud:string
Salidas: string
"""

def cargarMapa(divObjetivo, latitud, longitud):
	if not latitud or not longitud:
		latitud = "0"
		longitud = "0"
	cargarMapa = """
	<script language="JavaScript" type="text/javascript" charset="ISO-8859-1"
		src="http://maps.google.com/maps?file=api&amp;v=2&amp;key=""" +settings.LLAVE_GOOGLEMAPS+ """" type="text/javascript"></script>
	<script language="JavaScript" type="text/javascript" charset="ISO-8859-1">
	$(function()
	{
		if (GBrowserIsCompatible())
		{
			this.map = new GMap2(document.getElementById(\"""" +divObjetivo+ """"));
			this.map.setUIToDefault();
			this.map.setCenter(new GLatLng(""" +str(latitud)+ """, """ +str(longitud)+ """), 2);
			this.marker = new GMarker(new GLatLng(""" +str(latitud)+ """, """ +str(longitud)+ """), {clickable: false, draggable: false, title: 'aqui estoy | """ +settings.NOMBRE_APLICACION+ """'});
			this.map.addOverlay(this.marker);
		}
	});
	</script>
	"""
	return cargarMapa
register.simple_tag(cargarMapa)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion actualizarCoordenadasImagen: actualiza las coordenadas de la region seleccionada en una imagen
Entradas: imgObjetivo:string
Salidas: string
"""

def actualizarCoordenadasImagen(imgObjetivo):
	actualizarCoordenadasImagen = """
   <script type="text/javascript">
   	$(function()
      {
   		$(window).load(function()
         {
   			$("#""" +imgObjetivo+ """").imgAreaSelect({ aspectRatio: "1:1", onSelectEnd: actualizarCoordenadas });
   		});
   	});
   </script>
	"""
	return actualizarCoordenadasImagen
register.simple_tag(actualizarCoordenadasImagen)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion mostrarColoresDisponibles: muestra los colores de interfaz disponibles para elegir
Entradas: formularioObjetivo:string
Salidas: string
"""

def mostrarColoresDisponibles():
	mostrarColoresDisponibles = """
	<div id="div_seleccionColor">
		<div class="div_colorInterfaz" title="sabia savia | """ +settings.NOMBRE_APLICACION+ """" style="background:#808000;" onClick="return cambiarColorInterfaz('808000');">&nbsp;</div>
		<div class="div_colorInterfaz" title="sol solecito | """ +settings.NOMBRE_APLICACION+ """" style="background:#FFBB00;" onClick="return cambiarColorInterfaz('FFBB00');">&nbsp;</div>
		<div class="div_colorInterfaz" title="antares | """ +settings.NOMBRE_APLICACION+ """" style="background:#CC0000;" onClick="return cambiarColorInterfaz('CC0000');">&nbsp;</div>
		<div class="div_colorInterfaz" title="algod&oacute;n de az&uacute;car | """ +settings.NOMBRE_APLICACION+ """" style="background:#FF33CC;" onClick="return cambiarColorInterfaz('FF33CC');">&nbsp;</div>
		<div class="div_colorInterfaz" title="lim&oacute;n sin sal | """ +settings.NOMBRE_APLICACION+ """" style="background:#00CC00;" onClick="return cambiarColorInterfaz('00CC00');">&nbsp;</div>
		<div class="div_colorInterfaz" title="imperio real | """ +settings.NOMBRE_APLICACION+ """" style="background:#0011EE;" onClick="return cambiarColorInterfaz('0011EE');">&nbsp;</div>
		<div class="div_colorInterfaz" title="energ&iacute;a oscura | """ +settings.NOMBRE_APLICACION+ """" style="background:#333333;" onClick="return cambiarColorInterfaz('333333');">&nbsp;</div>
		<a href="#" title="cerrar | """ +settings.NOMBRE_APLICACION+ """" onClick="return mostrarSeleccionColor();">(X)</a>
	</div>
	"""
	return mostrarColoresDisponibles
register.simple_tag(mostrarColoresDisponibles)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion mostrarEnlacesPaginacion: retorna los enlaces necesarios para la navegacion entre paginas
Entradas: elementosSeleccionados:objeto
Salidas: string
"""

def mostrarEnlacesPaginacion(elementosSeleccionados, mensajeTotalElementos, numeroTotalElementos):
	# Determinando la pagina actual
	paginaActual = str(elementosSeleccionados.number)
	ultimaPagina = str(elementosSeleccionados.paginator.num_pages)
	enlaceAnterior = ''
	enlaceSiguiente = ''
	# Determinando si existen paginas anteriores
	if elementosSeleccionados.has_previous():
		numeroPaginaAnterior = elementosSeleccionados.previous_page_number()
		enlaceAnterior = '<a href="?pagina=1">primera</a>&nbsp;&middot;&nbsp;<a href="?pagina=' +str(numeroPaginaAnterior)+ '">anterior</a>&nbsp;&nbsp;&nbsp;' 
	# Determinando si existen paginas siguientes
	if elementosSeleccionados.has_next():
		numeroPaginaSiguiente = elementosSeleccionados.next_page_number()
		enlaceSiguiente = '&nbsp;&nbsp;&nbsp;<a href="?pagina=' +str(numeroPaginaSiguiente)+ '">siguiente</a>&nbsp;&middot;&nbsp;<a href="?pagina=' +ultimaPagina+ '">&uacute;ltima</a>' 	
	mostrarEnlacesPaginacion = """
	<div id="div_navegadorPaginas">
		<div id="div_numeroTotal"><b><u>""" +mensajeTotalElementos+ """</u></b>: """ +str(numeroTotalElementos)+ """</div>
		<div id="div_enlacesPaginas">
			""" +enlaceAnterior+ """
			<u>P&aacute;gina """ +paginaActual+ """ de """ +ultimaPagina+ """</u>
			""" +enlaceSiguiente+ """
		</div>
		<div class="div_limpiarZona"></div>
	</div>
	"""
	return mostrarEnlacesPaginacion
register.simple_tag(mostrarEnlacesPaginacion)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion determinarRangoUsuario: retorna una cadena que representa el rango del usuario actual
Entradas: numeroVisitas:int
Salidas: string
"""

def determinarRangoUsuario(numeroVisitas):
	numeroVisitas = int(numeroVisitas)
	if numeroVisitas in range(0,13):
		rangoUsuario = 'soy novato'
	elif numeroVisitas in range(13,33):
		rangoUsuario = 'he venido unas cuantas veces'
	elif numeroVisitas in range(33,77):
		rangoUsuario = 'vengo con fecuencia'		
	else:
		rangoUsuario = 'esta es mi casa y por aqu&iacute; siempre me encuentran'		
	return rangoUsuario
register.simple_tag(determinarRangoUsuario)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearEnlacesAmistad: retorna los enlaces adecuados para ubicar en el perfil publico y las busquedas de usuario
Entradas: usuarioPerfilActual:objeto, usuarioVisitante:objeto
Salidas: string
"""

def crearEnlacesAmistad(usuarioPerfilActual, usuarioVisitante):
	# Si trata de acceder un usuario en sesion actualmente
	if not usuarioVisitante.is_anonymous():
		if usuarioPerfilActual != usuarioVisitante:
			# Si el usuario actual esta viendo el perfil publico de un amigo
			if sonAmigos(usuarioPerfilActual, usuarioVisitante.username):
				crearEnlacesAmistad = crearMensajeLinealExito('&iexcl;Ya son amigos!')
			else:
				# Si existe una solicitud de amistad pendiente entre los usuarios involucrados
				if existeSolicitudAmistad(usuarioPerfilActual, usuarioVisitante.username):
					crearEnlacesAmistad = crearMensajeLinealAlerta('Amistad pendiente.')
				else:
					crearEnlacesAmistad = """
					<span id="span_enviarSolicitudAmistad">
					<a title="enviar una solicitud de amistad | """ +settings.NOMBRE_APLICACION+ """" href=\"""" +reverse('enlace_enviarSolicitudAmistad', args=[usuarioPerfilActual.username])+ """"
					onClick="return confirmacion_enviarSolicitudAmistad(this, '""" +usuarioPerfilActual.username+ """')">enviar una solicitud de amistad</a>
					</span>"""
		else:
			crearEnlacesAmistad = ''
	return crearEnlacesAmistad
register.simple_tag(crearEnlacesAmistad)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion crearEnlacePerfil: retorna el enlace adeacuado al perfil mas preciso
Entradas: usuarioPerfilActual:objeto, usuarioVisitante:objeto, textoEnlace:string
Salidas: string
"""

def crearEnlacePerfil(usuarioPerfilActual, usuarioVisitante, textoEnlace):
	# Si el usuario actual esta viendo el perfil publico de un amigo
	if sonAmigos(usuarioPerfilActual, usuarioVisitante.username):
		perfilAdecuado = 'enlace_mostrarPerfilExtendido'
	else:
		perfilAdecuado = 'enlace_mostrarPerfil_publico'
	crearEnlacePerfil = '<a title="ver perfil | ' +settings.NOMBRE_APLICACION+ '" href="' +reverse(perfilAdecuado, args=[usuarioPerfilActual.username])+ '" target="_blank">' +str(textoEnlace)+ '</a>'
	return crearEnlacePerfil
register.simple_tag(crearEnlacePerfil)

# ----------------------------------------------------------------------