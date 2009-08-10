# coding=latin-1

# --------------------------------------------------
"""
savia/manage.py
Julian Perez
Ultima modificacion: Abril 24 de 2009, 10:06
"""
# --------------------------------------------------



# -------------------------------------------------
""" Importaciones """

from django.core.management import execute_manager

# --------------------------------------------------

try:
	import settings
except ImportError:
	import sys
	sys.stderr.write("Error: Can't find the file 'settings.py'!")
	sys.exit(1)

if __name__ == "__main__":
	execute_manager(settings)

# --------------------------------------------------