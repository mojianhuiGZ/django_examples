#!/usr/bin/env python
import os
import sys

# WSGI config
#
# It exposes the WSGI callable as a module-level variable named `application`.
# For more information on this file, see
# https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

application = get_wsgi_application()


if __name__ == '__main__':
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
