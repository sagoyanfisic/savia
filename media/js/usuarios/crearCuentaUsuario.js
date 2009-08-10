/**
----------------------------------------------------------------------
---
savia/media/js/usuarios/crearCuentaUsuario.js
Julian Perez
Ultima modificacion: Abril 24 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------
/*
Funcion verificarNombreUsuario: verifica la disponibilidad del nombre de usuario digitado
Entradas: ninguna
Salidas: ninguna
*/

function verificarNombreUsuario()
{
	longitudMinima = 5;
	nombreElegido = $("form :input[name=nombreElegido]");
	nombreElegido.change(function ()
	{
		destinoFormulario = $('form').attr('action');
		if ( !nombreElegido.val() ) $('#span_verificarNombreElegido').html('&nbsp');
		else if ( nombreElegido.val().length<longitudMinima ) $('#span_verificarNombreElegido').html(crearMensajeLinealError('El nombre de usuario debe tener por lo menos ' +longitudMinima+ ' caracteres de longitud.'));
		else
		{
			$.ajax
			({
				type: 'POST',
				url: destinoFormulario+ 'consultarusuario/',
				data: 'nombreElegido=' +nombreElegido.val(),
				success: function(respuestaServidor)
				{
					if ( respuestaServidor=='respuestaServidor_exito' )
					{
						$('#span_verificarNombreElegido').html(crearMensajeLinealExito('Disponible.'));
					}
					else
					{
						$('#span_verificarNombreElegido').html(crearMensajeLinealError('No disponible.'));
					}
				}			
			});
		}
	});
}

// ----------------------------------------------------------------------