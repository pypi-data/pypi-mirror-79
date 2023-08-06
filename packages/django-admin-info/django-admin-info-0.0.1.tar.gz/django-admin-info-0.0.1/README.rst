=====
Django Admin Info
=====

Simple Collapsible Admin view for Django with model information.

Installation
-----------

    pip install django-admin-info


Quick start
-----------

1. Add "admin_info" to your INSTALLED_APPS in settings.py like this::

    INSTALLED_APPS = [
        ...
        'admin_info',
        ...
    ]

2. Ensure "APP_DIRS" to "True" in settings.py like this::
    TEMPLATES = [
        {
            ...
            'DIRS': [],
            'APP_DIRS': True,
            ...
        },
    ]


Licence
-----------
Copyright (c) 2020 Nilesh Kumar Dubey

This repository is licensed under the MIT license.
See LICENSE for details
