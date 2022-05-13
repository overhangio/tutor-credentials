credentials plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/lpm0073/tutor-contrib-credentials

Configuration
-------------

- ``CREDENTIALS_API_KEY`` (default: ``"{{ 20|random_string }}"``)
- ``CREDENTIALS_API_TIMEOUT`` (default: ``5``)
- ``CREDENTIALS_SECRET_KEY`` (default: ``"CHANGE-ME"``)
- ``CREDENTIALS_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}lpm0073/openedx-credentials:{{ CREDENTIALS_VERSION }}"``)
- ``CREDENTIALS_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)
- ``CREDENTIALS_HOST`` (default: ``"credentials.{{ LMS_HOST }}"``)
- ``CREDENTIALS_MFE_HOST`` (default: ``"apps.{{ LMS_HOST }}"``)
- ``CREDENTIALS_MYSQL_DATABASE`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_USERNAME`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_OAUTH2_KEY`` (default: ``"credentials"``)
- ``CREDENTIALS_OAUTH2_KEY_DEV`` (default: ``"credentials-dev"``)
- ``CREDENTIALS_OAUTH2_KEY_SSO`` (default: ``"credentials-sso"``)
- ``CREDENTIALS_OAUTH2_KEY_SSO_DEV`` (default: ``"credentials-sso-dev"``)
- ``CREDENTIALS_OAUTH2_SECRET`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_OAUTH2_SECRET_DEV`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_OAUTH2_SECRET_SSO`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_OAUTH2_SECRET_SSO_DEV`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_SECRET_KEY`` (default: ``"{{ 20|random_string }}"``)


Usage
-----

::

    tutor plugins enable credentials
    tutor config save --set CREDENTIALS_DOCKER_IMAGE=URI_OF_YOUR_REPOSITORY
    tutor images build credentials
    tutor images push credentials
    docker tag YOUR-IMAGE-NAME YOUR-IMAGE-NAME:latest
    docker push YOUR-IMAGE-NAME:latest

License
-------

This software is licensed under the terms of the AGPLv3.