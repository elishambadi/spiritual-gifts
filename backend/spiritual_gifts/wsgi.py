"""
WSGI config for spiritual_gifts project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spiritual_gifts.settings')

application = get_wsgi_application()
