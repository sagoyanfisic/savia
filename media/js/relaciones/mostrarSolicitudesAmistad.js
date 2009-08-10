/**
----------------------------------------------------------------------
---
savia/media/js/relaciones/mostrarSolicitudesAmistad.js
Julian Perez
Ultima modificacion: Agosto 07 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------
/*
Funcion confirmacion_aprobarSolicitudAmistad: crea un mensaje de alerta con confirmacion antes de aprobar una solicitud de amistad
Entradas: enlaceActual:objeto, nombreNuevoAmigo:string, numeroPaginaOrigen:string
Salidas: boolean
*/

function confirmacion_aprobarSolicitudAmistad(enlaceActual, nombreNuevoAmigo, numeroPaginaOrigen)
{
	urlAceptarSolicitud = $(enlaceActual).attr('href');
	titulo = 'aprobar una solicitud de amistad';
   mensaje = '&iexcl;Listo!<br/>Tu lista de amigos sigue creciendo... <i>si as&iacute; lo deseas</i>.<br/>Desde este momento, <u>' +nombreNuevoAmigo+ '</u> y t&uacute; ser&aacute;n amigos.';
   botones =
	{
		'no, mejor lo pienso bien': function() { $(this).dialog('close'); },
		'si, estoy de acuerdo': function() { window.location = urlAceptarSolicitud+ '?paginaOrigen=' + numeroPaginaOrigen; }
	};
	crearMensajeDesplegableExito(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion confirmacion_rechazarSolicitudAmistad: crea un mensaje de alerta con confirmacion antes de eliminar un amigo
Entradas: enlaceActual:objeto, nombreAmigoActual:string, numeroPaginaOrigen:string
Salidas: boolean
*/

function confirmacion_rechazarSolicitudAmistad(enlaceActual, nombreAmigoActual, numeroPaginaOrigen)
{
	urlRechazarSolicitud = $(enlaceActual).attr('href');
	titulo = 'rechazar una solicitud de amistad';
   mensaje = '&iexcl;Ten cuidado!<br/>Una amistad est&aacute; a punto de no concretarse... al menos <i>por ahora</i>.<br/><u>' +nombreAmigoActual+ '</u> y t&uacute; no podr&aacute;n ser amigos.';
   botones =
	{
		'no, mejor lo pienso bien': function() { $(this).dialog('close'); },
		'si, es lo que quiero': function() { window.location = urlRechazarSolicitud+ '?paginaOrigen=' + numeroPaginaOrigen; }
	};
	crearMensajeDesplegableError(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------