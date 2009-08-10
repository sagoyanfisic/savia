/**
----------------------------------------------------------------------
---
savia/media/js/almacenamiento/subirArchivo.js
Julian Perez
Ultima modificacion: Abril 24 de 2009, 23:05
---
----------------------------------------------------------------------
**/



// ----------------------------------------------------------------------

(function($)
{
	$.fn.uploadProgress = function(options)
	{
		options = $.extend(
		{
			dataType: "json",
			interval: 2000,
			progressBar: "#barraProgreso",
			progressUrl: "/almacenamiento/subirArchivo/progreso/",
			start: function() {},
			uploading: function() {},
			complete: function() {},
			success: function() {},
			error: function() {},
			preloadImages: [],
			uploadProgressPath: '/site_media/js/jquery/jquery.uploadProgress.js',
			jqueryPath: '/site_media/js/jquery/javascripts/jquery-1.3.2.min.js',
			timer: ""
		}, options);
		$(function()
		{
			for ( var i = 0; i<options.preloadImages.length; i++ )
			{
				options.preloadImages[i] = $("<img>").attr("src", options.preloadImages[i]);
			}
			if ( $.browser.safari && top.document==document )
			{
				iframe = document.createElement('iframe');
				iframe.name = "progressFrame";
				$(iframe).css({width: '0', height: '0', position: 'absolute', top: '-3000px'});
				document.body.appendChild(iframe);
				var d = iframe.contentWindow.document;
				d.open();
				d.write('<html><head></head><body></body></html>');
				d.close();
				var b = d.body;
				var s = d.createElement('script');
				s.src = options.jqueryPath;
				s.onload = function()
				{
					var s1 = d.createElement('script');
					s1.src = options.uploadProgressPath;
					b.appendChild(s1);
				}
				b.appendChild(s);
			}
		});
		return this.each(function()
		{
			$(this).bind('submit', function()
			{
				var uuid = "";
				for ( i = 0; i < 32; i++ )
				{
					uuid += Math.floor(Math.random() * 16).toString(16);
				}
				options.uuid = uuid;
				options.start();
				if ( old_id = /X-Progress-ID=([^&]+)/.exec($(this).attr("action")) )
				{
					var action = $(this).attr("action").replace(old_id[1], uuid);
					$(this).attr("action", action);
				}
				else
				{
					$(this).attr("action", jQuery(this).attr("action") + "?X-Progress-ID=" + uuid);
				}
				var uploadProgress = $.browser.safari ? progressFrame.jQuery.uploadProgress : jQuery.uploadProgress;
				options.timer = window.setInterval(function()
				{
					uploadProgress(this, options)
				},
				options.interval);
			});
		});
	};
	jQuery.uploadProgress = function(e, options)
	{
		jQuery.ajax(
		{
			type: "GET",
			url: options.progressUrl + "?archivoProgreso-ID=" + options.uuid,
			dataType: options.dataType,
			success: function(upload)
			{
				if ( upload.state == 'uploading' )
				{
					upload.percents = Math.floor((upload.received / upload.size)*1000)/10;
					var bar = $.browser.safari ? $(options.progressBar, parent.document) : $(options.progressBar);
					bar.css({width: upload.percents+'%'});
					options.uploading(upload);
				}
				if ( upload.state == 'done' || upload.state == 'error' )
				{
					window.clearTimeout(options.timer);
					options.complete(upload);
				}
				if ( upload.state == 'done' )
				{
					options.success(upload);
				}
				if ( upload.state == 'error' )
				{
					options.error(upload);
				}
			}
		});
	};
})(jQuery);

// ----------------------------------------------------------------------