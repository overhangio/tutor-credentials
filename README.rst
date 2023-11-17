Credentials plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `Credentials <https://github.com/openedx/credentials/>`__ application in an Open edX platform.
Credentials application supports course and program certificates. This plugin offers an admin panel where user can do configurations for the certificates of his course and program.

Note that user will have to create the course/program using `Discovery plugin <https://github.com/overhangio/tutor-discovery>`__. Then Credentials plugin will be used for certificates configurations.

.. image:: https://github.com/overhangio/tutor-credentials/blob/main/doc/django-admin-screen-shot.png
    :alt: Django Admin

Installation
------------

::

    pip install https://github.com/overhangio/tutor-credentials.git

Note that this plugin is compatible with `Kubernetes integration <http://docs.tutor.overhang.io/k8s.html>`__.


For further instructions on how to setup Credentials with Open edX, check the `Official Credentials documentation <https://readthedocs.org/projects/edx-credentials/>`__.

Usage
-----

::

    pip install tutor-credentials
    tutor plugins enable discovery mfe credentials
    tutor local launch

For Copying programs that user make in `Discovery plugin <https://github.com/overhangio/tutor-discovery>`__ into Credentials. Run the below command:
::

    tutor local run credentials ./manage.py copy_catalog

Using Django Admin
~~~~~~~~~~~~~~~~~~

The credentials user interface will be available at http://credentials.local.overhang.io for a local instance, and at ``CREDENTIALS_HOST`` (by  default: ``http(s)://credentials.<your lms host>``) in production. In order to run commands from the UI login with an admin user at: http://credentials.local.overhang.io/admin/. User should be able to authenticate with the same username and password that he used for his lms.
User can also create superuser for credentials using the below command
::

    tutor local run credentials ./manage.py createsuperuser

Configuration
-------------

Application configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_HOST`` (default: ``"credentials.{{ LMS_HOST }}"``)
- ``CREDENTIALS_MYSQL_DATABASE`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_USERNAME`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}overhangio/openedx-credentials:{{ CREDENTIALS_VERSION }}"``)
- ``CREDENTIALS_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)
- ``CREDENTIALS_SITE_NAME`` (default: ``"LMS_HOST"``)
- ``CREDENTIALS_REPOSITORY`` (default: ``"https://github.com/openedx/credentials.git"``)
- ``CREDENTIALS_REPOSITORY_VERSION`` (default: ``"{{ OPENEDX_COMMON_VERSION }}"``)

Marketing & Theming
~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_LOGO_TRADEMARK_URL`` (default: ``"https://edx-cdn.org/v3/default/logo-trademark.svg"``)
- ``CREDENTIALS_LOGO_TRADEMARK_URL_PNG`` (default: ``"https://edx-cdn.org/v3/default/logo-trademark.png"``)
- ``CREDENTIALS_LOGO_TRADEMARK_URL_SVG`` (default: ``"https://edx-cdn.org/v3/default/logo-trademark.svg"``)
- ``CREDENTIALS_LOGO_URL`` (default: ``"https://edx-cdn.org/v3/default/logo.svg"``)
- ``CREDENTIALS_LOGO_URL_PNG`` (default: ``"https://edx-cdn.org/v3/default/logo.png"``)
- ``CREDENTIALS_LOGO_URL_SVG`` (default: ``"https://edx-cdn.org/v3/default/logo.svg"``)
- ``CREDENTIALS_LOGO_WHITE_URL`` (default: ``"https://edx-cdn.org/v3/default/logo-white.svg"``)
- ``CREDENTIALS_LOGO_WHITE_URL_PNG`` (default: ``"https://edx-cdn.org/v3/default/logo-white.png"``)
- ``CREDENTIALS_LOGO_WHITE_URL_SVG`` (default: ``"https://edx-cdn.org/v3/default/logo-white.svg"``)
- ``CREDENTIALS_FAVICON_URL`` (default: ``"https://edx-cdn.org/v3/default/favicon.ico"``)
- ``CREDENTIALS_THEME_NAME`` (default: ``"edx-theme"``)

Backend authentication
~~~~~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_KEY`` (default: ``"credentials-backend-service-key"``)
- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_SECRET`` (default: ``"{{ CREDENTIALS_OAUTH2_SECRET }}"``)
- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL`` (default: ``"http://lms:8000/oauth2"``)
- ``CREDENTIALS_OAUTH2_KEY``  (default: ``credentials-backend-service-key"``)
- ``CREDENTIALS_OAUTH2_SECRET`` (default: ``"CHANGE-ME"``)

Application Third party authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_SOCIAL_AUTH_REDIRECT_IS_HTTPS`` (default: ``{% if ENABLE_HTTPS %}True{% else %}False{% endif %}``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_ISSUER`` (default: ``"{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT`` (default: ``"http://lms:8000"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_KEY`` (default: ``"credentials-sso-key"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_SECRET`` (default: ``"credentials-sso-secret"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL`` (default: ``"{{ SOCIAL_AUTH_EDX_OAUTH2_ISSUER }}/logout"``)

Funding
-------

.. image:: https://www.academiacentral.org/wp-content/uploads/2019/05/academia-nobeta.png
    :alt: Academia Central
    :target: https://www.academiacentral.org/

This plugin was initially developed and open sourced to the community thanks to the generous support of `Academia Central <https://www.academiacentral.org/>`_. Thank you!

License
-------

This software is licensed under the terms of the AGPLv3.
