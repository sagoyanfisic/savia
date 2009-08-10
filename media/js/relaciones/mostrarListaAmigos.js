/**
----------------------------------------------------------------------
---
savia/media/js/relaciones/mostrarAmistades.js
Julian Perez
Ultima modificacion: Agosto 07 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------
/*
Funcion modificarEstadoAmistad: elimina el avatar actual y reemplaza la iamgen con el avatar generico, desde la plantilla de mensajes recibidos
Entradas: enlaceActual:objeto
Salidas: ninguna
*/

function modificarEstadoAmistad(enlaceActual)
{
	elementoActual = $(enlaceActual);
	$.ajax
	({
		type: 'POST',
		url: elementoActual.attr('href'),
		data: '',
		success: function(respuestaServidor)
		{
			if ( respuestaServidor == 'respuestaServidor_exito' )
			{
				imagenActual = elementoActual.children('img');
				rutaImagen_1 = imagenActual.attr('src').split('_')[0];
				rutaImagen_2 = imagenActual.attr('src').split('_')[1];
				archivoActual = imagenActual.attr('src').split('_')[2];
				if ( archivoActual == 'ordinario.gif' )
				{
					imagenActual.attr('src', rutaImagen_1+ '_' +rutaImagen_2+ '_importante.gif');
					elementoActual.parent().parent().attr('class','tr_amistadDestacada');
				}
				if ( archivoActual == 'importante.gif' )
				{
					imagenActual.attr('src', rutaImagen_1+ '_' +rutaImagen_2+ '_ordinario.gif');
					elementoActual.parent().parent().attr('class','tr_amistadRegular');
				}
			}
		}
	});
	elementoActual.blur();
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion confirmacion_eliminarAmistad: crea un mensaje de alerta con confirmacion antes de eliminar un amigo
Entradas: enlaceActual:objeto, nombreAmigoActual:string, numeroPaginaOrigen:string
Salidas: boolean
*/

function confirmacion_eliminarAmistad(enlaceActual, nombreAmigoActual, numeroPaginaOrigen)
{
	urlEliminarAmistad = $(enlaceActual).attr('href');
	titulo = 'eliminar este amigo';
   mensaje = '&iexcl;Ten cuidado!<br/>Cabeza fr&iacute;a debes tener, porque esta operaci&oacute;n es <i>irreversible</i>.<br/><u>' +nombreAmigoActual+ '</u> y t&uacute; ya no ser&aacute;n amigos.';
   botones =
	{
		'no, mejor lo conservo': function() { $(this).dialog('close'); },
		'sí, eliminar este amigo': function() { window.location = urlEliminarAmistad+ '?paginaOrigen=' + numeroPaginaOrigen; }
	};
	crearMensajeDesplegableError(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------