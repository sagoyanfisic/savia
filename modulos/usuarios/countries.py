# coding=latin-1

# ----------------------------------------------------------------------
"""
savia/modulos/usuarios/countries.py
Julian Perez
Ultima modificacion: Agosto 02 de 2009, 10:36
"""
# ----------------------------------------------------------------------



# ----------------------------------------------------------------------
""" Importaciones """

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
""" Variables globales para este archivo """

# Lista de los paises disponibles
COUNTRIES = (
	('ZZ', _('-sin establecer-')),
	('AD', _('Andorra')),
	('AE', _('Emiratos Arabes Unidos')),
	('AF', _('Afganistan')),
	('AG', _('Antigua y Barbuda')),
	('AI', _('Anguilla')),
	('AL', _('Albania')),
	('AM', _('Armenia')),
	('AN', _('Antillas Holandesas')),
	('AO', _('Angola')),
	('AQ', _('Antartica')),
	('AR', _('Argentina')),
	('AS', _('Samoa Americana')),
	('AT', _('Austria')),
	('AU', _('Australia')),
	('AW', _('Aruba')),
	('AZ', _('Azerbaijan')),
	('BA', _('Bosnia y Herzegovina')),
	('BB', _('Barbados')),
	('BD', _('Bangladesh')),
	('BE', _('Belgica')),
	('BF', _('Burkina Faso')),
	('BG', _('Bulgaria')),
	('BH', _('Bahrein')),
	('BI', _('Burundi')),
	('BJ', _('Benin')),
	('BM', _('Bermuda')),
	('BN', _('Brunei Darussalam')),
	('BO', _('Bolivia')),
	('BR', _('Brasil')),
	('BS', _('Bahamas')),
	('BT', _('Butan')),
	('BV', _('Bouvet, Isla')),
	('BW', _('Botswana')),
	('BY', _('Belarus')),
	('BZ', _('Belice')),
	('CA', _('Canada')),
	('CC', _('Cocos (Keeling), Islas')),
	('CF', _('Republica Central Africana')),
	('CG', _('Congo')),
	('CH', _('Suiza')),
	('CI', _('Costa de Marfil')),
	('CK', _('Cook, Islas')),
	('CL', _('Chile')),
	('CM', _('Camerun')),
	('CN', _('China')),
	('CO', _('Colombia')),
	('CR', _('Costa Rica')),
	('CU', _('Cuba')),
	('CV', _('Cabo Verde')),
	('CX', _('Christmas, Isla')),
	('CY', _('Chipre')),
	('CZ', _('Republica Checa')),
	('DE', _('Alemania')),
	('DJ', _('Djibouti')),
	('DK', _('Dinamarca')),
	('DM', _('Dominica')),
	('DO', _('Republica Dominicana')),
	('DZ', _('Algeria')),
	('EC', _('Ecuador')),
	('EE', _('Estonia')),
	('EG', _('Egipto')),
	('EH', _('Sahara Occidental')),
	('ER', _('Eritrea')),
	('ES', _(u'España')),
	('ET', _('Etiopia')),
	('FI', _('Finlandia')),
	('FJ', _('Fiji')),
	('FK', _('Falkland (Malvinas), Islas')),
	('FM', _('Micronesia')),
	('FO', _('Faroe, Islas')),
	('FR', _('Francia')),
	('GA', _('Gabon')),
	('GB', _('Reino Unido')),
	('GD', _('Granada')),
	('GE', _('Georgia')),
	('GF', _('Guayana Francesa')),
	('GH', _('Ghana')),
	('GI', _('Gibraltar')),
	('GL', _('Groenlandia')),
	('GM', _('Gambia')),
	('GN', _('Guinea')),
	('GP', _('Guadalupe')),
	('GQ', _('Guinea Ecuatorial')),
	('GR', _('Grecia')),
	('GS', _('Georgia del Sur y Sandwich del Sur, Islas')),
	('GT', _('Guatemala')),
	('GU', _('Guam')),
	('GW', _('Guinea-Bissau')),
	('GY', _('Guyana')),
	('HK', _('Hong Kong')),
	('HM', _('Heard y McDonald, Islas')),
	('HN', _('Honduras')),
	('HR', _('Croacia')),
	('HT', _('Haiti')),
	('HU', _('Hungria')),
	('ID', _('Indonesia')),
	('IE', _('Irlanda')),
	('IL', _('Israel')),
	('IN', _('India')),
	('IO', _('Terrotorio Oceanico de las Indias Britanicas')),
	('IQ', _('Irak')),
	('IR', _('Iran')),
	('IS', _('Islandia')),
	('IT', _('Italia')),
	('JM', _('Jamaica')),
	('JO', _('Jordania')),
	('JP', _('Japon')),
	('KE', _('Kenia')),
	('KG', _('Kyrgyzstan')),
	('KH', _('Camboya')),
	('KI', _('Kiribati')),
	('KM', _('Comoros')),
	('KN', _('St. Kitts y Nevis')),
	('KP', _('Corea del Norte')),
	('KR', _('Corea del Sur')),
	('KW', _('Kuwait')),
	('KY', _('Cayman, Islas')),
	('KZ', _('Kazakhstan')),
	('LA', _('Laos')),
	('LB', _('Libano')),
	('LC', _('Saint Lucia')),
	('LI', _('Liechtenstein')),
	('LK', _('Sri Lanka')),
	('LR', _('Liberia')),
	('LS', _('Lesotho')),
	('LT', _('Lituania')),
	('LU', _('Luxemburgo')),
	('LV', _('Latvia')),
	('LY', _('Libia')),
	('MA', _('Marruecos')),
	('MC', _('Monaco')),
	('MD', _('Moldavia')),
	('MG', _('Madagascar')),
	('MH', _('Marshall, Islas')),
	('ML', _('Mali')),
	('MN', _('Mongolia')),
	('MM', _('Myanmar')),
	('MO', _('Macau')),
	('MP', _('Mariana del Norte, Islas')),
	('MQ', _('Martinica')),
	('MR', _('Mauritania')),
	('MS', _('Monserrate')),
	('MT', _('Malta')),
	('MU', _('Mauricio')),
	('MV', _('Maldivas')),
	('MW', _('Malawi')),
	('MX', _('Mexico')),
	('MY', _('Malasia')),
	('MZ', _('Mozambique')),
	('NA', _('Namibia')),
	('NC', _('Nueva Caledonia')),
	('NE', _('Niger')),
	('NF', _('Norfolk, Isla')),
	('NG', _('Nigeria')),
	('NI', _('Nicaragua')),
	('NL', _('Holanda (Paises Bajos)')),
	('NO', _('Noruega')),
	('NP', _('Nepal')),
	('NR', _('Nauru')),
	('NU', _('Niue')),
	('NZ', _('Nueva Zelanda')),
	('OM', _('Oman')),
	('PA', _('Panama')),
	('PE', _('Peru')),
	('PF', _('Polinesia Francesa')),
	('PG', _('Papua Nueva Guinea')),
	('PH', _('Filipinas')),
	('PK', _('Pakistan')),
	('PL', _('Polonia')),
	('PM', _('St. Pierre & Miquelon')),
	('PN', _('Pitcairn')),
	('PR', _('Puerto Rico')),
	('PT', _('Portugal')),
	('PW', _('Palau')),
	('PY', _('Paraguay')),
	('QA', _('Qatar')),
	('RE', _('Reunion')),
	('RO', _('Rumania')),
	('RU', _('Rusia')),
	('RW', _('Rwanda')),
	('SA', _('Arabia Saudita')),
	('SB', _('Solomon, Islas')),
	('SC', _('Seychelles')),
	('SD', _('Sudan')),
	('SE', _('Suecia')),
	('SG', _('Singapur')),
	('SH', _('St. Helena')),
	('SI', _('Eslovenia')),
	('SJ', _('Svalbard y Jan Mayen, Islas')),
	('SK', _('Eslovaquia')),
	('SL', _('Sierra Leona')),
	('SM', _('San Marino')),
	('SN', _('Senegal')),
	('SO', _('Somalia')),
	('SR', _('Suriname')),
	('ST', _('Sao Tome y Principe')),
	('SV', _('El Salvador')),
	('SY', _('Siria')),
	('SZ', _('Swaziland')),
	('TC', _('Turks y Caicos, Islas')),
	('TD', _('Chad')),
	('TF', _('Territorios Franceses del Sur')),
	('TG', _('Togo')),
	('TH', _('Tailandia')),
	('TJ', _('Tajikistan')),
	('TK', _('Tokelau')),
	('TM', _('Turkmenistan')),
	('TN', _('Tunez')),
	('TO', _('Tonga')),
	('TP', _('Timor Oriental')),
	('TR', _('Turquia')),
	('TT', _('Trinidad y Tobago')),
	('TV', _('Tuvalu')),
	('TW', _('Taiwan')),
	('TZ', _('Tanzania')),
	('UA', _('Ucrania')),
	('UG', _('Uganda')),
	('US', _('Estados Unidos de America')),
	('UY', _('Uruguay')),
	('UZ', _('Uzbekistan')),
	('VA', _('Ciudad del Vaticano')),
	('VC', _('St. Vincent y las Granadinas')),
	('VE', _('Venezuela')),
	('VG', _('Virgines Britanicas, Islas')),
	('VI', _('Virgines Americanas, Islas')),
	('VN', _('Vietnam')),
	('VU', _('Vanuatu')),
	('WF', _('Wallis y Futuna, Islas')),
	('WS', _('Samoa')),
	('YE', _('Yemen')),
	('YT', _('Mayotte')),
	('YU', _('Yugoslavia')),
	('ZA', _('Sudafrica')),
	('ZM', _('Zambia')),
	('ZR', _('Zaire')),
	('ZW', _('Zimbabwe')),
)

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Funcion isValidCountry: determina si el campo CountryField es valido
Entradas: field_data, all_data
Salidas: objeto(ValidationError)
"""

def isValidCountry(field_data, all_data):
	if not field_data in [lang[0] for lang in COUNTRIES]:
		raise ValidationError, _('This value must be in COUNTRIES setting in localflavor.generic package.')

# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
"""
Clase save: procesa el formulario de tipo RecuperarContrasenaFormulario, enviando el mensaje de recuperacion por correo electronico
Entradas: el mismo formulario, domain_override:string, email_template_name:string, use_https:boolean, token_generator:objeto(default_token_generator)
Salidas: ninguna
"""

class CountryField(CharField):

	"""
	Funcion __init__: constructor de la clase CountryField
	Entradas: ninguna
	Salidas: ninguna
	"""
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('max_length', 2)
		kwargs.setdefault('choices', COUNTRIES)
		super(CharField, self).__init__(*args, **kwargs)

	"""
	Funcion get_internal_type: retorna el tipo de campo asociado a la clase CountryField
	Entradas: el mismo campo, ninguna
	Salidas: string
	"""
	def get_internal_type(self):
		return 'CharField'

# ----------------------------------------------------------------------