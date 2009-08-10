/**
----------------------------------------------------------------------
---
savia/media/js/relaciones/mostrarMensajes.js
Julian Perez
Ultima modificacion: Agosto 03 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------
/*
Funcion modificarEstadoMensaje_bandeja: modifica el estado del mensaje seleccionado, desde la plantilla de mensajes recibidos
Entradas: enlaceActual:objeto
Salidas: ninguna
*/

function modificarEstadoMensaje_bandeja(enlaceActual)
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
				}
				if ( archivoActual == 'importante.gif' )
				{
					imagenActual.attr('src', rutaImagen_1+ '_' +rutaImagen_2+ '_ordinario.gif');
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
Funcion modificarEstadoMensaje_mensaje: modifica el estado del mensaje seleccionado, desde la plantilla de mensaje
Entradas: enlaceActual:objeto
Salidas: ninguna
*/

function modificarEstadoMensaje_mensaje(enlaceActual)
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
				tituloMensaje = $('#span_tituloMensaje');
				tipoMensaje = tituloMensaje.attr("class");
				if ( tipoMensaje=='span_mensajeOrdinario' )
				{
					tituloMensaje.attr('class', 'span_mensajeImportante');
				}
				if ( tipoMensaje == 'span_mensajeImportante' )
				{
					tituloMensaje.attr('class', 'span_mensajeOrdinario');
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
Funcion confirmacion_eliminarMensaje: crea un mensaje de alerta con confirmacion antes de eliminar un mensaje
Entradas: enlaceActual:objeto, numeroPaginaOrigen:string
Salidas: boolean
*/

function confirmacion_eliminarMensaje(enlaceActual, numeroPaginaOrigen)
{
	urlEliminarMensaje = $(enlaceActual).attr('href');
	titulo = 'eliminar este mensaje';
   mensaje = 'Ohhh no... vas a eliminar un mensaje.<br/>Pi&eacute;nsalo bien, ya que esta operaci&oacute;n es <i>irreversible</i>.<br/>&iquest;<u>Est&aacute;s seguro</u>?';
   botones =
	{
		'no, mejor lo pienso bien': function() { $(this).dialog('close'); },
		'sí, eliminar el mensaje': function() { window.location = urlEliminarMensaje+ '?paginaOrigen=' + numeroPaginaOrigen; }
	};
	crearMensajeDesplegableError(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------