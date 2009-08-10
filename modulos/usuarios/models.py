# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/usuarios/models.py
Julian Perez
Ultima modificacion: Marzo 18 de 2009, 23:36
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

import os
import datetime
from django.conf import settings
from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales para este archivo """

GENEROS = ( ('z', '-sin establecer-'), ('f', 'Femenino'), ('m', 'Masculino'), )
PAISES_DISPONIBLES = (
	('ZZ', '-sin establecer-'),
	('AD', 'Andorra'), ('AE', 'Emiratos Arabes Unidos'), ('AF', 'Afganistan'), ('AG', 'Antigua y Barbuda'), ('AI', 'Anguilla'), ('AL', 'Albania'), ('AM', 'Armenia'), ('AN', 'Antillas Holandesas'),
	('AO', 'Angola'), ('AQ', 'Antartica'), ('AR', 'Argentina'), ('AS', 'Samoa Americana'), ('AT', 'Austria'), ('AU', 'Australia'), ('AW', 'Aruba'), ('AZ', 'Azerbaijan'), ('BA', 'Bosnia y Herzegovina'),
	('BB', 'Barbados'), ('BD', 'Bangladesh'), ('BE', 'Belgica'), ('BF', 'Burkina Faso'), ('BG', 'Bulgaria'), ('BH', 'Bahrein'), ('BI', 'Burundi'), ('BJ', 'Benin'), ('BM', 'Bermuda'), ('BN', 'Brunei Darussalam'),
	('BO', 'Bolivia'), ('BR', 'Brasil'), ('BS', 'Bahamas'), ('BT', 'Butan'), ('BV', 'Bouvet, Isla'), ('BW', 'Botswana'), ('BY', 'Belarus'), ('BZ', 'Belice'), ('CA', 'Canada'), ('CC', 'Cocos (Keeling), Islas'),
	('CF', 'Republica Central Africana'), ('CG', 'Congo'), ('CH', 'Suiza'), ('CI', 'Costa de Marfil'), ('CK', 'Cook, Islas'), ('CL', 'Chile'), ('CM', 'Camerun'), ('CN', 'China'), ('CO', 'Colombia'),
	('CR', 'Costa Rica'), ('CU', 'Cuba'), ('CV', 'Cabo Verde'), ('CX', 'Christmas, Isla'), ('CY', 'Chipre'), ('CZ', 'Republica Checa'), ('DE', 'Alemania'), ('DJ', 'Djibouti'), ('DK', 'Dinamarca'), ('DM', 'Dominica'),
	('DO', 'Republica Dominicana'), ('DZ', 'Algeria'), ('EC', 'Ecuador'), ('EE', 'Estonia'), ('EG', 'Egipto'), ('EH', 'Sahara Occidental'), ('ER', 'Eritrea'), ('ES', u'España'), ('ET', 'Etiopia'), ('FI', 'Finlandia'),
	('FJ', 'Fiji'), ('FK', 'Falkland (Malvinas), Islas'), ('FM', 'Micronesia'), ('FO', 'Faroe, Islas'), ('FR', 'Francia'), ('GA', 'Gabon'), ('GB', 'Reino Unido'), ('GD', 'Granada'), ('GE', 'Georgia'),
	('GF', 'Guayana Francesa'), ('GH', 'Ghana'), ('GI', 'Gibraltar'), ('GL', 'Groenlandia'), ('GM', 'Gambia'), ('GN', 'Guinea'), ('GP', 'Guadalupe'), ('GQ', 'Guinea Ecuatorial'), ('GR', 'Grecia'),
	('GS', 'Georgia del Sur y Sandwich del Sur, Islas'), ('GT', 'Guatemala'), ('GU', 'Guam'), ('GW', 'Guinea-Bissau'), ('GY', 'Guyana'), ('HK', 'Hong Kong'), ('HM', 'Heard y McDonald, Islas'), ('HN', 'Honduras'),
	('HR', 'Croacia'), ('HT', 'Haiti'), ('HU', 'Hungria'), ('ID', 'Indonesia'), ('IE', 'Irlanda'), ('IL', 'Israel'), ('IN', 'India'), ('IO', 'Terrotorio Oceanico de las Indias Britanicas'), ('IQ', 'Irak'), ('IR', 'Iran'), ('IS', 'Islandia'),
	('IT', 'Italia'), ('JM', 'Jamaica'), ('JO', 'Jordania'), ('JP', 'Japon'), ('KE', 'Kenia'), ('KG', 'Kyrgyzstan'), ('KH', 'Camboya'), ('KI', 'Kiribati'), ('KM', 'Comoros'), ('KN', 'St. Kitts y Nevis'), ('KP', 'Corea del Norte'),
	('KR', 'Corea del Sur'), ('KW', 'Kuwait'), ('KY', 'Cayman, Islas'), ('KZ', 'Kazakhstan'), ('LA', 'Laos'), ('LB', 'Libano'), ('LC', 'Saint Lucia'), ('LI', 'Liechtenstein'), ('LK', 'Sri Lanka'), ('LR', 'Liberia'),
	('LS', 'Lesotho'), ('LT', 'Lituania'), ('LU', 'Luxemburgo'), ('LV', 'Latvia'), ('LY', 'Libia'), ('MA', 'Marruecos'), ('MC', 'Monaco'), ('MD', 'Moldavia'), ('MG', 'Madagascar'), ('MH', 'Marshall, Islas'), ('ML', 'Mali'),
	('MN', 'Mongolia'), ('MM', 'Myanmar'), ('MO', 'Macau'), ('MP', 'Mariana del Norte, Islas'), ('MQ', 'Martinica'), ('MR', 'Mauritania'), ('MS', 'Monserrate'), ('MT', 'Malta'), ('MU', 'Mauricio'), ('MV', 'Maldivas'),
	('MW', 'Malawi'), ('MX', 'Mexico'), ('MY', 'Malasia'), ('MZ', 'Mozambique'), ('NA', 'Namibia'), ('NC', 'Nueva Caledonia'), ('NE', 'Niger'), ('NF', 'Norfolk, Isla'), ('NG', 'Nigeria'), ('NI', 'Nicaragua'),
	('NL', 'Holanda (Paises Bajos)'), ('NO', 'Noruega'), ('NP', 'Nepal'), ('NR', 'Nauru'), ('NU', 'Niue'), ('NZ', 'Nueva Zelanda'), ('OM', 'Oman'), ('PA', 'Panama'), ('PE', 'Peru'), ('PF', 'Polinesia Francesa'),
	('PG', 'Papua Nueva Guinea'), ('PH', 'Filipinas'), ('PK', 'Pakistan'), ('PL', 'Polonia'), ('PM', 'St. Pierre & Miquelon'), ('PN', 'Pitcairn'), ('PR', 'Puerto Rico'), ('PT', 'Portugal'), ('PW', 'Palau'),
	('PY', 'Paraguay'), ('QA', 'Qatar'), ('RE', 'Reunion'), ('RO', 'Rumania'), ('RU', 'Rusia'), ('RW', 'Rwanda'), ('SA', 'Arabia Saudita'), ('SB', 'Solomon, Islas'), ('SC', 'Seychelles'), ('SD', 'Sudan'),
	('SE', 'Suecia'), ('SG', 'Singapur'), ('SH', 'St. Helena'), ('SI', 'Eslovenia'), ('SJ', 'Svalbard y Jan Mayen, Islas'), ('SK', 'Eslovaquia'), ('SL', 'Sierra Leona'), ('SM', 'San Marino'), ('SN', 'Senegal'),
	('SO', 'Somalia'), ('SR', 'Suriname'), ('ST', 'Sao Tome y Principe'), ('SV', 'El Salvador'), ('SY', 'Siria'), ('SZ', 'Swaziland'), ('TC', 'Turks y Caicos, Islas'), ('TD', 'Chad'), ('TF', 'Territorios Franceses del Sur'),
	('TG', 'Togo'), ('TH', 'Tailandia'), ('TJ', 'Tajikistan'), ('TK', 'Tokelau'), ('TM', 'Turkmenistan'), ('TN', 'Tunez'), ('TO', 'Tonga'), ('TP', 'Timor Oriental'), ('TR', 'Turquia'), ('TT', 'Trinidad y Tobago'),
	('TV', 'Tuvalu'), ('TW', 'Taiwan'), ('TZ', 'Tanzania'), ('UA', 'Ucrania'), ('UG', 'Uganda'), ('US', 'Estados Unidos de America'), ('UY', 'Uruguay'), ('UZ', 'Uzbekistan'), ('VA', 'Ciudad del Vaticano'),
	('VC', 'St. Vincent y las Granadinas'), ('VE', 'Venezuela'), ('VG', 'Virgines Britanicas, Islas'), ('VI', 'Virgines Americanas, Islas'), ('VN', 'Vietnam'), ('VU', 'Vanuatu'), ('WF', 'Wallis y Futuna, Islas'),
	('WS', 'Samoa'), ('YE', 'Yemen'), ('YT', 'Mayotte'), ('YU', 'Yugoslavia'), ('ZA', 'Sudafrica'), ('ZM', 'Zambia'), ('ZR', 'Zaire'), ('ZW', 'Zimbabwe'),
)
TEMAS_DISPONIBLES = ( ('808000', 'Sabia savia'), ('FFBB00', 'Sol solecito'), ('FF0000', 'Antares'), ('FF33CC', 'Algodon de azucar'), ('00CC00', 'Limon sin sal'), ('0011EE', 'Imperio real'), ('333333', 'Energia oscura'), )

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase Perfil: define el modelo de gestion de los perfiles de usuarios
Entradas: hereda de Model, ninguna
"""

class Perfil(models.Model):

	# Campos disponibles para el modelo Perfil
	user = models.ForeignKey(User, unique=True, verbose_name='usuario asociado')
	sexo = models.CharField('Sexo', max_length=1, choices=GENEROS, blank=True, default='z')
	fechaNacimiento = models.DateField('Fecha de nacimiento', default=datetime.date.today())
	url = models.URLField('URL personal', blank=True, default='http://www.savia.com/')
	acerca = models.TextField(u'Acerca de mí', blank=True, default='-acerca de mi-')	
	pais = models.CharField(u'País', max_length=2, choices=PAISES_DISPONIBLES, blank=True, default='ZZ')
	lugar = models.CharField(u'Lugar', max_length=255, blank=True, default='-sin establecer-')
	latitud = models.DecimalField('Latitud', max_digits=10, decimal_places=6, blank=True, default=0)
	longitud = models.DecimalField('Longitud', max_digits=10, decimal_places=6, blank=True, default=0)
	numeroVisitas = models.IntegerField(u'Números de visitas', default=0)
	temaPreferido = models.CharField('Tema preferido', max_length=6, choices=TEMAS_DISPONIBLES, blank=True, default='808000')	

	# Valores meta de la clase Perfil
	class Meta:
		verbose_name_plural = 'Perfiles'

	"""
	Funcion __unicode__: retorna la representacion por defecto de la clase Perfil
	Entradas: el mismo modelo
	Salidas: string
	"""
	def __unicode__(self):
		return '%s' % self.user
		

	"""
	Funcion tieneAvatar: consulta y retorna el numero de objetos tipo Avatar (en caso de existir el avatar, debe ser 1) para el usuario actual, y que sean validos
	Entradas: el mismo modelo
	Salidas: int
	"""
	def tieneAvatar(self):
		return Avatar.objects.filter(usuarioAsociado=self.user, esValida=True).count()

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion destinoAvatares: determina la ruta adecuada para almacenar un avatar
Entradas: instancia:objeto, nombreArchivo:string
Salidas: string
"""
	
def destinoAvatares(instancia, nombreArchivo):
	return settings.DESTINO_AVATARES+ '%s' % nombreArchivo

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase Avatar: define el modelo de gestion de los avatares de usuarios
Entradas: hereda de Model, ninguna
"""

class Avatar(models.Model):

	# Campos disponibles para el modelo Avatar
	usuarioAsociado = models.ForeignKey(User, verbose_name='usuario asociado')
	imagen = models.ImageField('Imagen', upload_to=destinoAvatares)
	fechaHoraCreacion = models.DateTimeField(u'Fecha y hora de creación', default=datetime.datetime.now())
	esValida = models.BooleanField(u'¿Es válida la imagen?')

	# Valores meta de la clase Avatar
	class Meta:
		verbose_name_plural = 'Avatares'
		unique_together = (('usuarioAsociado', 'esValida'),)

	"""
	Funcion __unicode__: retorna la representacion por defecto de una instancia de la clase Perfil
	Entradas: el mismo modelo
	Salidas: string
	"""
	def __unicode__(self):
		return '%s' % self.usuarioAsociado

	"""
	Funcion save: almacena el avatar de un usuario
	Entradas: el mismo modelo
	Salidas: ninguna
	"""
	def save(self):
		for avatar in Avatar.objects.filter(usuarioAsociado=self.usuarioAsociado, esValida=self.esValida).exclude(id=self.id):
			base, filename = os.path.split(avatar.imagen.path)
			name, extension = os.path.splitext(filename)
			avatar.delete()
		super(Avatar, self).save()

# ----------------------------------------------------------------------