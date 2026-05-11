"""
WSGI config for uncle_shop project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os  # import os for setting environment variables

from django.core.wsgi import get_wsgi_application  # import WSGI application maker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uncle_shop.settings')  # set the default Django settings module

application = get_wsgi_application()  # create the WSGI application callable
