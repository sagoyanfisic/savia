# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/settings.py
Julian Perez
Ultima modificacion: Junio 18 de 2009, 10:06
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import os.path
from ConfigParser import RawConfigParser

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales de control creadas por defecto """

DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
	('Julian Perez', 'jcpmmx@gmail.com'),
	('Eduardo Aragon', 'earagon87@gmail.com'),
)
MANAGERS = ADMINS
TIME_ZONE = 'America/Bogota'
LANGUAGE_CODE = 'es-CO'
SITE_ID = 1
USE_I18N = True
SECRET_KEY = '8!ue&!b&1jf1c!fieig7u+#rcp%maoyr8gjm!p3d)47%jkua-$'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales de control creadas para savia """

NOMBRE_APLICACION = 'savia'
VERSION_APLICACION = 'v0.7a'

# Ruta generica de la carpeta de savia
RUTA_LOCAL = os.path.dirname(os.path.abspath(__file__))

# Eligiendo el sistema adecuado para cargar los datos locales
NOMBRE_INI = 'confbd_desarrollo.ini'
URL_PREFIJO = ''
	
MEDIA_ROOT = os.path.join(RUTA_LOCAL, 'media')
MEDIA_URL = URL_PREFIJO+ '/site_media/'
ADMIN_MEDIA_PREFIX = URL_PREFIJO+ '/media/'
AUTH_PROFILE_MODULE = 'usuarios.Perfil'
LOGIN_URL = URL_PREFIJO+ '/error403/'
# Accesos directos a las URLS principales
URL_CSS = MEDIA_URL+ 'css/'
URL_JS = MEDIA_URL+ 'js/'
URL_IMG = MEDIA_URL+ 'img/'
URL_IMGTMP = MEDIA_URL+ 'img/tmp/'
URL_IMGDCE = MEDIA_URL+ 'img/dce/'
URL_FNT = MEDIA_URL+ 'fnt/'
# Accesos directos a las rutas principales
RUTA_CSS = os.path.join(MEDIA_ROOT, 'css/')
RUTA_JS = os.path.join(MEDIA_ROOT, 'js/')
RUTA_IMG = os.path.join(MEDIA_ROOT, 'img/')
RUTA_IMGTMP = os.path.join(RUTA_IMG, 'tmp/')
RUTA_IMGDCE = os.path.join(RUTA_IMG, 'dce/')
RUTA_FNT = os.path.join(MEDIA_ROOT, 'fnt/')

# Determina cuantos objetos por pagina muestra el paginador
NUMERO_OBJETOS_PAGINA = 7

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Datos locales de configuracion de la base de datos """

# Cargando el archivo de datos locales
INI_LOCAL = os.path.join(RUTA_LOCAL, 'configuracion', NOMBRE_INI )
configuraciones = RawConfigParser()
configuraciones.read(INI_LOCAL)

# Instanciando los parametros para conectarse a la base de datos
DATABASE_ENGINE = configuraciones.get('basedatos', 'bd_motor')
DATABASE_NAME = configuraciones.get('basedatos', 'bd_nombre')
DATABASE_USER = configuraciones.get('basedatos', 'bd_usuario')
DATABASE_PASSWORD = configuraciones.get('basedatos', 'bd_contrasena')
DATABASE_HOST = configuraciones.get('basedatos', 'bd_maquina')
DATABASE_PORT = configuraciones.get('basedatos', 'bd_puerto')

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Control de los templates y de los middlewares instalados """

# Procesadores de contextos
TEMPLATE_CONTEXT_PROCESSORS = (
	'django.core.context_processors.auth',
	'django.core.context_processors.debug',
	'django.core.context_processors.i18n',
	'django.core.context_processors.media',
	'savia.modulos.utilidades.contexto.inicializarContexto',
)

# Carga del sistema de templates
TEMPLATE_LOADERS = (
	'django.template.loaders.filesystem.load_template_source',
	'django.template.loaders.app_directories.load_template_source',
	#'django.template.loaders.eggs.load_template_source',
)

# Directorio de ubicacion de los templates (plantillas)
TEMPLATE_DIRS = (
	os.path.join(RUTA_LOCAL, 'plantillas'),
)

# Middlewares instalados
MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Control de todo el enrutamiento necesario en savia """

ROOT_URLCONF = 'savia.modulos.general.urls'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Aplicaciones de Dajngo y propias instaladas en savia """

INSTALLED_APPS = (

	# Aplicaciones instaladas disponibles en Django
	'django.contrib.auth',
	'django.contrib.humanize',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.admin',
	# Aplicaciones creadas para savia
	'savia.modulos.general',
	'savia.modulos.usuarios',
	'savia.modulos.relaciones',
	'savia.modulos.almacenamiento',
	'savia.modulos.utilidades',

)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables de control del envio de correos electronicos """

# Configuracion para savia.proy@gmail.com
NOMBRE_CORREO = 'autocorreo | savia'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'savia.proy'
EMAIL_HOST_PASSWORD = 'saviachapu'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables de control del modulo de gestion de usuarios """

I18N_URLS = False
RUTA_AVATARES = os.path.join(RUTA_IMG, 'avt')
DESTINO_AVATARES = 'img/avt/' 
AVATAR_GENERICO = 'avt_generico.png'
RUTA_AVATAR_GENERICO = os.path.join(RUTA_IMG, AVATAR_GENERICO)
URL_AVATAR_GENERICO = URL_IMG + AVATAR_GENERICO
LLAVE_GOOGLEMAPS = 'ABQIAAAAhjQoA5dU4ad8jpv0zV2LDRSYTOrO14iwvK5JHvhTm4YZiKcsdRQVY_2SbI5skHAnNNxkLBZxAl_XGg'
# Llave de Google Maps que depende del dominio donde savia funcione
# - Si es http://localhost:8000 > ABQIAAAAhjQoA5dU4ad8jpv0zV2LDRQCULP4XOMyhPd8d_NrQQEO8sT8XBQFNB7A7o1caaQYrWY3OSEcm6j7LQ
# - Si es http://savia/ > ABQIAAAAhjQoA5dU4ad8jpv0zV2LDRRfIZlMesuG57_EVFrgdbH9hJrUSRSHnFtOOBaGojBsTekj40zThCfhhA
# - Si es http://vmlabs03.eisc.univalle.edu.co/savia/ > ABQIAAAAhjQoA5dU4ad8jpv0zV2LDRSYTOrO14iwvK5JHvhTm4YZiKcsdRQVY_2SbI5skHAnNNxkLBZxAl_XGg

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables de control del modulo de relaciones """

NOMBRE_USUARIO_ADMIN = 'savia'
NOMBRE_USUARIO_ANONIMO = 'anonimo'

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables de control del modulo de almacenamiento """

DESTINO_ARCHIVOS = 'esp'

# ----------------------------------------------------------------------