/**
----------------------------------------------------------------------
---
savia/media/js/usuarios/mostrarPerfil.js
Julian Perez
Ultima modificacion: Agosto 07 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------
/*
Funcion confirmacion_enviarSolicitudAmistad: crea un mensaje de alerta con confirmacion antes de enviar una solicitud de amistad
Entradas: enlaceActual:objeto, nombreUsuarioObjetivo:string
Salidas: boolean
*/

function confirmacion_enviarSolicitudAmistad(enlaceActual, nombreUsuarioObjetivo)
{
	urlEnviarSolicitudAmistad = $(enlaceActual).attr('href');
	titulo = 'enviar una solicitud de amistad';
	mensaje = '&iexcl;Listo!<br/>Un nuevo amigo <i>est&aacute; en camino</i>.<br/><u>' +nombreUsuarioObjetivo+ '</u> recibir&aacute; tu solicitud de amistad y decidir&aacute;.';
   botones =
	{
		'no, por ahora': function() { $(this).dialog('close'); },
		's�, eso es lo que quiero': function() { $(this).dialog('close'); enviarSolicitudAmistad(urlEnviarSolicitudAmistad); }
	};
	crearMensajeDesplegableExito(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion enviarSolicitudAmistad: envia la solicitud de amistad
Entradas: urlActual:string
Salidas: ninguna
*/

function enviarSolicitudAmistad(urlActual)
{
	$.ajax
	({
		type: 'POST',
		url: urlActual,
		data: '',
		success: function(respuestaServidor)
		{
			if ( respuestaServidor == 'respuestaServidor_exito' )
			{
				$('#span_enviarSolicitudAmistad').html(crearMensajeLinealExito('La solicitud fue enviada.'));
			}
		}
	});
	return false;
}

// ----------------------------------------------------------------------