"""
ASGI config for spiritual_gifts project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiritual_gifts.settings')

application = get_asgi_application()
