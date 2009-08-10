/**
----------------------------------------------------------------------
---
savia/media/js/base.js
Julian Perez
Ultima modificacion: Abril 24 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------
/*
Funcion establecerInterfaz: oculta la capa de informacion del error de Javascipt deshabilitado y establece la interfaz normal
Entradas: ninguna
Salidas: ninguna
*/

function establecerInterfaz()
{
	// Mostrando la pagina cubierta y la del mensaje
	$('#div_capaCubierta').css('visibility', 'hidden');
	$('#div_capaMensajes').css('visibility', 'hidden');
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion mostrarIndicadorAjax: muestra la barra indicadora de carga entre el servidor y el cliente
Entradas: ninguna
Salidas: boolean
*/

function mostrarIndicadorAjax()
{
	$('#div_indicadorPrincipal').css('visibility','visible');
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion ocultarIndicadorAjax: oculta la barra indicadora de carga entre el servidor y el cliente
Entradas: ninguna
Salidas: boolean
*/

function ocultarIndicadorAjax()
{
	$('#div_indicadorPrincipal').css('visibility','hidden');
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion habilitarIndicadorAjax: muestra la barra indicadora de carga entre el servidor y el cliente en eventos Ajax
Entradas: ninguna
Salidas: ninguna
*/

function habilitarIndicadorAjax()
{
	$(document)
	.ajaxStart(function()
	{
		$('#div_indicadorPrincipal').css('visibility','visible');
	})
	.ajaxStop(function()
	{
		ocultarIndicadorAjax();
	})
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion mostrarOcultarElemento: muestra y oculta un elemento objetivo
Entradas: idElementoObjetivo:string
Salidas: boolean
*/

function mostrarOcultarElemento(idElementoObjetivo)
{
	$('#' +idElementoObjetivo).slideToggle('slow');
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion mostrarSeleccionColor: muestra los colores disponibles
Entradas: ninguna
Salidas: boolean
*/

function mostrarSeleccionColor()
{
	mostrarOcultarElemento('div_seleccionColor');
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion cambiarColorInterfaz: cambia el color principal de la interfaz
Entradas: temaElegido:string
Salidas: boolean
*/

function cambiarColorInterfaz(temaElegido)
{
	// Cambiando el tema
	$('#div_contenedorPrincipal').css('background', '#' +temaElegido);
	// Registrando el cambio de color
	$.ajax
	({
		type: 'POST',
		url: URL_CAMBIAR_TEMA,
		data: 'temaElegido=' +temaElegido,
		success: function(respuestaServidor)
		{
			if ( respuestaServidor!='respuestaServidor_exito' )
			{
				$('#div_contenedorPrincipal').css('background', '#808000');
			}
		}		
	});
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion otorgarFoco: otorga el foco al elemento especifico referenciado con el ID
Entradas:idElemento:string
Salidas: ninguna
*/

function otorgarFoco(idElemento)
{
	// Busca el elemto y le otorga el foco actual
	$('#' +idElemento).focus();
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion construirElementoTabular: oculta el mensaje actual y reestablece la interfaz normal
Entradas:ninguna
Salidas: boolean
*/

function construirElementoTabular(idElemento)
{
	$('#' +idElemento).accordion(
	{
		animated: 'bounceslide'
	});
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion mostrarMensaje: muestra el mensaje actual con la interfaz de mensajes
Entradas:ninguna
Salidas: ninguna
*/

function mostrarMensaje()
{
	// Mostrando la pagina cubierta y la del mensaje
	$('#div_capaCubierta').css('visibility', 'visible');
	$('#div_capaMensajes').css('visibility', 'visible');
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion ocultarMensaje: oculta el mensaje actual y reestablece la interfaz normal
Entradas:ninguna
Salidas: boolean
*/

function ocultarMensaje()
{
	// Ocultando la capa cubierta y la del mensaje
	$('#div_capaCubierta').css('visibility', 'hidden');
	$('#div_capaMensajes').css('visibility', 'hidden');
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion centrarBloque: toma un elemento existente y lo ubica en posicion central, tanto horizontal como verticalmente
Entradas:elementoObjetivo:object(DOM)
Salidas: ninguna
*/

function centrarBloque(elementoObjetivo)
{
	anchoBloque = elementoObjetivo.width();
	alturaBloque = elementoObjetivo.height();
	if ( anchoBloque%2 != 0 ) anchoBloque++;
	if ( alturaBloque%2 != 0 ) alturaBloque++;
	elementoObjetivo.css('position', 'fixed');
	elementoObjetivo.css('top', '50%');
	elementoObjetivo.css('left', '50%');
	elementoObjetivo.css('margin-top', '-' +alturaBloque/2+ 'px');
	elementoObjetivo.css('margin-left', '-' +anchoBloque/2+ 'px');
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion crearMensajeDesplegable: crea un mensaje especifico y lo muestra
Entradas:tipoMensaje:string, textoMensaje:string, botonesMensaje:string
Salidas: llamado a la funcion mostrarMensaje
*/

function crearMensajeDesplegable(tipoMensaje, tituloMensaje, textoMensaje, botonesMensaje)
{
	// Capturando en un objeto la capa de mensajes
	mensaje = '<div id="div_cuadroMensaje" title="' +tituloMensaje+ ' | ' +NOMBRE_APLICACION+ '"><p class="p_textoMensajeDesplegable ' +tipoMensaje+ '">' +textoMensaje+ '</p></div>';
	$(mensaje).dialog(
	{
		width: 777,
		minHeight: 77,
		draggable: false,
		resizable: false,
		modal: true,
		buttons: botonesMensaje
	});
	//centrarBloque($('.ui-dialog'));
}

function crearMensajeDesplegableExito(tituloMensaje, textoMensaje, botonesMensaje)
{
   crearMensajeDesplegable('exito', tituloMensaje, textoMensaje, botonesMensaje);
}

function crearMensajeDesplegableError(tituloMensaje, textoMensaje, botonesMensaje)
{
   crearMensajeDesplegable('error', tituloMensaje, textoMensaje, botonesMensaje);
}

function crearMensajeDesplegableAlerta(tituloMensaje, textoMensaje, botonesMensaje)
{
   crearMensajeDesplegable('alerta', tituloMensaje, textoMensaje, botonesMensaje);
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion crearMensajeLineal: crea un mensaje de estado lineal
Entradas:tipo:string, mensaje:string
Salidas: string
*/

function crearMensajeLineal(tipoMensaje, textoMensaje)
{
	return '<span class="div_iconoEstado ' +tipoMensaje+'">&nbsp;&nbsp;&nbsp;</span><span class="p_mensajeEstadoLineal ' +tipoMensaje+ '">' +textoMensaje+ '</span>';
}

function crearMensajeLinealExito(textoMensaje)
{
	return crearMensajeLineal('exito', textoMensaje);
}

function crearMensajeLinealError(textoMensaje)
{
	return crearMensajeLineal('error', textoMensaje);
}

function crearMensajeLinealAlerta(textoMensaje)
{
	return crearMensajeLineal('alerta', textoMensaje);
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion confirmacion_terminarSesion: crea un mensaje de alerta con confirmacion antes de cerrar la sesion
Entradas:ninguna
Salidas: boolean
*/

function confirmacion_terminarSesion()
{
	titulo = 'terminar sesi&oacute;n';
   mensaje = 'Ohhh no... parece que quieres irte.<br/>A&uacute;n hay <i>mucho m&aacute;s</i> por hacer.<br/>&iquest;<u>Est&aacute;s seguro</u>?';
   botones =
	{
		'no, aquí me quedo': function() { $(this).dialog('close'); },
		'sí, terminar la sesión': function() { window.location = URL_TERMINAR_SESION; }
	};
	crearMensajeDesplegableAlerta(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion obtenerFormatoEsperadoCampo: retorna una descripcion del formato esperado para el campo especifico
Entradas:campoFormulario:objeto(HTML>input)
Salidas: string
*/

function obtenerFormatoEsperadoCampo(campoFormulario)
{
	descripcionCampo = '';
	tipoCampo = $(campoFormulario).attr('type');
	if ( tipoCampo=='' ) tipoCampo = $(campoFormulario).attr('tagname');
	switch ( tipoCampo )
	{
		case 'text': descripcionCampo += 'Texto (caracteres alfanum&eacute;ricos)'; break;
		case 'password': descripcionCampo += 'Texto de contrase&ntilde;a'; break;
		case 'textarea': descripcionCampo += 'Area de texto (caracteres alfanum&eacute;ricos)'; break;
		case 'select-one': descripcionCampo += 'Cuadro de selecci&oacute;n (opci&oacute;n &uacute;nica)'; break;
		case 'file': descripcionCampo += 'Cuadro de navegaci&oacute;n para subir un archivo'; break;
		default: break;
	}
	tamanoCampo = $(campoFormulario).attr('maxlength');
	if ( tamanoCampo>0 ) descripcionCampo += ', ' +tamanoCampo+ ' caracter(es) m&aacute;ximo';
	return descripcionCampo+ '.';
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion validarFormulario_completo: valida un formulario de manera generica desde el lado del cliente
Entradas:ninguna
Salidas: boolean
*/

function validarFormulario_completo()
{
	nombreCampoActual = '';
	nombresCamposIncorrectos = '';
	// Capturando todos los campos del formulario actual, excluyendo el boton de envio
	camposDisponibles = $('form :input[type!=submit][class!=noCapturar]');
	// Capturando el boton de envio del formulario actual
	botonEnvio = $('form :input[type=submit]');
	numeroCamposDisponibles  = camposDisponibles.length;
	for ( idx=0; idx<numeroCamposDisponibles; idx++ ) 
	{
		campoActual = $(camposDisponibles[idx]);
		nombreCampoActual = $(':label [for=' +campoActual.attr("id")+ ']').html();
		if ( $(campoActual).val()=="" )
		{
			nombresCamposIncorrectos += '<u>' +nombreCampoActual+ '</u> Campo obligatorio. ' +obtenerFormatoEsperadoCampo(campoActual)+ ' <br/>';
		}
	}
	if ( nombresCamposIncorrectos=='' )
	{
		mostrarAnimacionFormulario_iniciaAjax();
		mostrarIndicadorAjax();
		return true;
	}
	else
	{
		titulo = $(botonEnvio).val();
		mensaje = 'Antes de presionar el bot&oacute;n <i>' +titulo+ '</i>, verifica los siguientes campos del formulario:<br/><br/>';
		mensaje2 = nombresCamposIncorrectos;
		botones =
		{
			'vale, tendré más cuidado': function() { $(this).dialog('close'); }
		};
		crearMensajeDesplegableError(titulo, mensaje+mensaje2, botones);
		return false;
	}
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion construirFormularioAjax: contruye un formulario (parejas de datos tipo 'nombreCampo' = valor) de manera generica desde el lado del cliente
Entradas:ninguna
Salidas: string
*/

function construirFormularioAjax()
{
	// Capturando todos los campos del formulario actual, con sus valores actuales
	camposDisponibles = $('form').serialize();
	return camposDisponibles;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion mostrarAnimacion_iniciaAjax: aplica una animacion cuando inicia una operacion Ajax a un objeto especifico
Entradas: ninguna
Salidas: ninguna
*/

function mostrarAnimacionFormulario_iniciaAjax()
{
	$('form').fadeTo('slow', 0.23);
	//$('form :input[type=submit]').attr('disabled', 'disabled');
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion mostrarAnimacionFormulario_finalAjax: aplica una animacion cuando finaliza una operacion Ajax a un objeto especifico
Entradas: ninguna
Salidas: ninguna
*/

function mostrarAnimacionFormulario_finalAjax()
{
	$('form').fadeTo('slow', 1);
	$('form :input[type=submit]').removeAttr('disabled');
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion construirFormularioAjax: contruye un formulario (parejas de datos tipo 'nombreCampo' = valor) de manera generica desde el lado del cliente
Entradas: ninguna
Salidas: boolean
*/

function enviarFormularioAjax()
{
	// Primero se valida el formulario desde el cliente
	esValido = validarFormulario_completo();
	//  El formulario se procesa en el servidor si y solo si es valido
	if ( esValido )
	{
		destinoFormulario = $('form').attr('action');
		datosFormulario = construirFormularioAjax();
		mostrarAnimacionFormulario_iniciaAjax();
		$.ajax
		({
			type: 'POST',
			url: destinoFormulario,
			data: datosFormulario,
			success: function(respuestaServidor)
			{
				//alert(respuestaServidor.responseText);
				if ( respuestaServidor=='respuestaServidor_exito' )
				{
					mostrarAnimacionFormulario_finalAjax();
					mostrarMensajeEstado(destinoFormulario+ URL_EXITO);
				}
				else
				{
					mostrarAnimacionFormulario_finalAjax();
					mensajeErrorServidor = procesarErrorServidor(respuestaServidor);
					mostrarMensajeEstado_error(mensajeErrorServidor);
				}
			},
			error: function(respuestaServidor)
			{
				//alert(respuestaServidor.responseText);
				mostrarAnimacionFormulario_finalAjax();
				mostrarMensajeEstado_error(ERROR_SERVIDOR);
			}			
		});
	}
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion irAtras: se devuelve a la pagina anterior (como el boton 'Atras' de los navegadores)
Entradas: ninguna
Salidas: boolean
*/

function irAtras()
{
	history.back();
	return false;
}

// ----------------------------------------------------------------------