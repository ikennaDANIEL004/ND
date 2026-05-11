"""
ASGI config for uncle_shop project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os  # import os for setting environment variables

from django.core.asgi import get_asgi_application  # import ASGI application maker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uncle_shop.settings')  # set the default settings module for Django

application = get_asgi_application()  # create the ASGI application callable
