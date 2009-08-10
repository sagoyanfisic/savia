/**
----------------------------------------------------------------------
---
savia/media/js/usuarios/editarPerfil.js
Julian Perez
Ultima modificacion: Abril 24 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion cargarImagenGenero: carga la imagen adecuada segun el valor actual del genero del usuario
Entradas:generoActual:string
Salidas:ninguna
*/

function cargarImagenGenero(generoActual)
{
	if ( !generoActual || generoActual=='z' ) generoActual = "d";
	switch ( generoActual )
	{		
		case 'f': alternativo = "sexo: femenino | " +NOMBRE_APLICACION; titulo = "sexo: femenino | " +NOMBRE_APLICACION; break;
		case 'm': alternativo = "sexo: masculino | " +NOMBRE_APLICACION; titulo = "sexo: masculino | " +NOMBRE_APLICACION; break;
		case 'd': alternativo = "sexo: sin establecer | " +NOMBRE_APLICACION; titulo = "sexo: sin establecer | " +NOMBRE_APLICACION; break;
	}
	$('#img_sexo').attr({ src: URL_IMG+ 'genero_' +generoActual+ '.png', alt: alternativo, title: titulo });
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion cambiarImagenGenero: carga la imagen adecuada cuando cambie el valor del genero del usuario
Entradas:ninguna
Salidas: llamado a la funcion cargarImagenGenero
*/

function cambiarImagenGenero()
{
	img_sexo = $('#id_sexo');
	img_sexo.change(function ()
	{
		cargarImagenGenero(img_sexo.val());
	});
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion verificarValidezImagen: verifica si la imagen cumple con las dimensiones minimas
Entradas: img:objetoHTML, regionSeleccionada:objetoHTML
Salidas: ninguna
*/

function verificarValidezImagen()
{
	validezImagen = $('input[name=editarPerfil_avatar_validez]').val();
	if ( validezImagen=='esValida' ) return true;
	else
	{
		botonEnvio = $('form :input[type=submit]');
		titulo = $(botonEnvio).val();
		regionSeleccionada = $('input[name=derecha]').val()-$('input[name=izquierda]').val();
		mensajeRegionSeleccionada = regionSeleccionada+ 'x' +regionSeleccionada+ ' pixeles';
		mensaje = 'Hay alg&uacute;n error con la regi&oacute;n seleccionada de la imagen... antes de reintentarlo, por favor verifica:<br/>';
		mensaje2 = '<br/><u>Imagen</u> - Selecciona una regi&oacute;n de dimensiones v&aacute;lidas.<br/>(Actualmente has seleccionado ' +mensajeRegionSeleccionada+ '... son necesarios al menos 96x96 pixeles).<br/>'
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
Funcion confirmacion_eliminarMensaje: crea un mensaje de alerta con confirmacion antes de eliminar un mensaje
Entradas: enlaceActual:objeto, rutaGenerico:string
Salidas: boolean
*/

function confirmacion_eliminarAvatar(enlaceActual, rutaGenerico)
{
	titulo = 'eliminar mi avatar';
   mensaje = '&iexcl;Ten cuidado!<br/>Te vas a quedar sin avatar... al menos <i>por ahora</i>.<br/><u>No tendr&aacute;s</u> una imagen que te represente.';
   botones =
	{
		'no, mejor lo pienso bien': function() { $(this).dialog('close'); },
		'sí, así está bien': function(){ $(this).dialog('close'); eliminarAvatar(enlaceActual, rutaGenerico); }
	};
	crearMensajeDesplegableError(titulo, mensaje, botones);
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion eliminarAvatar: elimina el avatar actual y reemplaza la iamgen con el avatar generico
Entradas: enlaceActual:objeto, rutaGenerico:string
Salidas: ninguna
*/

function eliminarAvatar(enlaceActual, rutaGenerico)
{
	elementoActual = $(enlaceActual);
	$.ajax
	({
		type: 'POST',
		url: elementoActual.attr('href'),
		data: '',
		success: function(respuestaServidor)
		{
			if ( respuestaServidor=='respuestaServidor_exito' )
			{
				$('#img_avatar').attr('src', rutaGenerico);
				$('#div_eliminarAvatar').html(crearMensajeLinealExito('El avatar actual fue eliminado satisfactoriamente.'));
			}
		}			
	});		
	elementoActual.blur();	
	return false;
}

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funciones necesarias para el mapa de ubicacion
*/

function mapFramework()
{
	if (GBrowserIsCompatible())
	{
		this.map = new GMap2(document.getElementById("div_mapaUbicacion"));
		this.map.enableContinuousZoom();
		this.map.setUIToDefault();
		var lat = lng = 0;
		if ($("#id_latitud").val()) lat = $("#id_latitud").val();
		if ($("#id_longitud").val()) lng = $("#id_longitud").val();
		this.map.setCenter(new GLatLng(lat, lng), 4);
		this.marker = new GMarker(new GLatLng(lat, lng), {clickable: false, bouncy: true, draggable: true, title: 'aquí estás! | savia'}); 
		this.map.addOverlay(this.marker);
		GEvent.addListener(this.marker, "dragend", function()
		{
			var point = this.getLatLng();
			$("#id_latitud").val(point.lat().toFixed(6));
			$("#id_longitud").val(point.lng().toFixed(6));
			destinoFormulario = $('form').attr('action');
			$.getJSON(URL_OBTENER_CIUDAD+'?latitud=' +point.lat()+ '&longitud=' + point.lng(), function(data)
			{
				$("#id_pais").val(data['pais']);
				$("#id_lugar").val(data['lugar']);
			});
		});
	}
}

mapFramework.prototype.searchLocation = function()
{
	address = $("#id_pais option:selected").text();
 	geocoder = new GClientGeocoder();
	var g = this;
 	geocoder.getLatLng(address, function(point)
	{
 		if ( !point ) point = new GLatLng(0.000000,0.000000);
		g.map.setCenter(point);
		g.marker.setLatLng(point);
		$("#id_latitud").val(point.lat().toFixed(6));
		$("#id_longitud").val(point.lng().toFixed(6));
		destinoFormulario = $('form').attr('action');
		$.getJSON(URL_OBTENER_CIUDAD+'?latitud=' +point.lat()+ '&longitud=' + point.lng(), function(data)
		{
			$("#id_pais").val(data['pais']);
			$("#id_lugar").val(data['lugar']);
		});
 	}); 
}

var googlemaps;

function initMap()
{
	googlemaps = new mapFramework();
	googlemaps.searchLocation();
}

function initMap2()
{
	googlemaps = new mapFramework();
}

$(function()
{
	$("#id_pais").change(function()
	{
		if ( !$("#id_pais option:selected").val() || $("#id_pais option:selected").val()=='ZZ')
		{
			$("#id_lugar").val('-sin establecer-');
			$("#id_latitud").val('0');
			$("#id_longitud").val('0');
		}
		googlemaps.searchLocation();
	});
	if ( $("#id_pais option:selected").val() )
	{
      $.getScript("http://maps.google.com/maps?file=api&v=2.x&key=" + $("#div_llaveGoogleMaps").text() + "&async=2&callback=initMap2");
	}
	else
	{
		$("#id_lugar").val('-sin establecer-');
		$("#id_latitud").val(0);
		$("#id_longitud").val('0');
		return;		
	}
});

// ----------------------------------------------------------------------

// ----------------------------------------------------------------------
/*
Funcion actualizarCoordenadas: elimina el avatar actual y reemplaza la iamgen con el avatar generico
Entradas: img:objetoHTML, regionSeleccionada:objetoHTML
Salidas: ninguna
*/

function actualizarCoordenadas(img, regionSeleccionada)
{
	// Procesando las coordenadas para evitar numeros decimales (solo se aceptan enteros)
	if ( regionSeleccionada.y1%2==0.5 || regionSeleccionada.y1%2==1.5 ) arriba = regionSeleccionada.y1-0.5;
	else arriba = regionSeleccionada.y1;
	if ( regionSeleccionada.y2%2==0.5 || regionSeleccionada.y2%2==1.5 ) abajo = regionSeleccionada.y2-0.5;
	else abajo = regionSeleccionada.y2;	
	if ( regionSeleccionada.x1%2==0.5 || regionSeleccionada.x1%2==1.5 ) izquierda = regionSeleccionada.x1-0.5;
	else izquierda = regionSeleccionada.x1;	
	if ( regionSeleccionada.x2%2==0.5 || regionSeleccionada.x2%2==1.5 ) derecha = regionSeleccionada.x2-0.5;
	else derecha = regionSeleccionada.x2;
	// Actualizando los valores de las coordenadas
	$('form :input[name=arriba]').val(parseInt(arriba));
	$('form :input[name=abajo]').val(parseInt(abajo));
	$('form :input[name=izquierda]').val(parseInt(izquierda));
	$('form :input[name=derecha]').val(parseInt(derecha));
	// Verificando que la region seleccionada sea de al menos 96x96 pixeles y validando ese resultado
	if ( (derecha-izquierda)<96 )
	{
		$("form :input[name='editarPerfil_avatar_validez']").val('esInvalida');
	}
	else
	{
		$("form :input[name='editarPerfil_avatar_validez']").val('esValida');
	}
}

// ----------------------------------------------------------------------