"""
ASGI config for her_beauty_hub project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'her_beauty_hub.settings')

application = get_asgi_application()

