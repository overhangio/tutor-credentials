credentials plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/lpm0073/tutor-contrib-credentials

Configuration
-------------

- ``CREDENTIALS_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}lpm0073/openedx-credentials:{{ CREDENTIALS_VERSION }}"``)
- ``CREDENTIALS_SECRET_KEY`` (default: ``"CHANGE-ME"``)
- ``CREDENTIALS_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)
- ``CREDENTIALS_HOST`` (default: ``"credentials.{{ LMS_HOST }}"``)
- ``CREDENTIALS_MYSQL_DATABASE`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_USERNAME`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
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
- ``CREDENTIALS_SOCIAL_AUTH_REDIRECT_IS_HTTPS`` (default: ``{% if ENABLE_HTTPS %}True{% else %}False{% endif %}``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_ISSUER`` (default: ``"{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT`` (default: ``"http://lms:8000"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_KEY`` (default: ``"credentials-sso-key"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_SECRET`` (default: ``"credentials-sso-secret"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL`` (default: ``"{{ SOCIAL_AUTH_EDX_OAUTH2_ISSUER }}/logout"``)
- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_KEY`` (default: ``"credentials-backend-service-key"``)
- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_SECRET`` (default: ``"{{ CREDENTIALS_OAUTH2_SECRET }}"``)
- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL`` (default: ``"http://lms:8000/oauth2"``)



Usage
-----

::

    # tutor local
    tutor plugins enable credentials

    # tutor on k8s
    # you'll need to create a public remote repository (ie AWS ECR)
    # ---------------------------------------------------------------------
    tutor plugins enable credentials
    tutor config save --set CREDENTIALS_DOCKER_IMAGE=URI_OF_YOUR_REPOSITORY
    tutor images build credentials
    tutor images push credentials
    docker tag YOUR-IMAGE-NAME YOUR-IMAGE-NAME:latest
    docker push YOUR-IMAGE-NAME:latest

License
-------

This software is licensed under the terms of the AGPLv3.