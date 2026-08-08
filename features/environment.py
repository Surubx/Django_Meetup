import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meetup_site.settings_test')

import django
from django.core.management import call_command

django.setup()
call_command('migrate', verbosity=0, interactive=False)
