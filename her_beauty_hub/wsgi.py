"""
WSGI config for her_beauty_hub project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')

application = get_wsgi_application()

