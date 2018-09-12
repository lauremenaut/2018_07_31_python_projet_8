#! /usr/bin/env python3
# coding: utf-8

"""
WSGI config for pur_beurre_lm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pur_beurre_lm.settings')

application = get_wsgi_application()
