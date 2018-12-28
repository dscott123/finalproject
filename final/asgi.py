import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "final.settings")
django.setup()
applictaion = get_default_application()