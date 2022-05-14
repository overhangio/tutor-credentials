credentials plugin for `Tutor <https://docs.tutor.overhang.io>`__
===================================================================================

This is a plugin for `Tutor <https://docs.tutor.overhang.io>`_ that integrates the `Credentials <https://github.com/openedx/certificates/>`__ application in an Open edX platform.
This plugin also syncs the credentials database core_user table to openedx.auth_user, so after installing you should be able to authenticate with the same credentials that you use for your lms.

Installation
------------

::

    pip install git+https://github.com/lpm0073/tutor-contrib-credentials

This plugin requires tutor>=12.0.0, the `Discovery plugin <https://github.com/overhangio/tutor-discovery>`__ and the `MFE plugin <https://github.com/overhangio/tutor-mfe>`__. If you have installed Tutor by downloading the pre-compiled binary, then both plugins should be automatically installed. You can confirm by running::

    tutor plugins list

Then, in any case you need to enable the plugins::

    tutor plugins enable discovery mfe credentials

Services will have to be re-configured and restarted, so you are probably better off just running quickstart again::

    tutor local quickstart

Note that this plugins is compatible with `Kubernetes integration <http://docs.tutor.overhang.io/k8s.html>`__. When deploying to a Kubernetes cluster run instead, noting that you'll need to create a public remote repository (ie AWS ECR)::

    tutor plugins enable discovery mfe credentials
    tutor config save --set CREDENTIALS_DOCKER_IMAGE=URI_OF_YOUR_REPOSITORY
    tutor images build credentials
    tutor images push credentials
    docker tag YOUR-IMAGE-NAME YOUR-IMAGE-NAME:latest
    docker push YOUR-IMAGE-NAME:latest
    tutor k8s quickstart


For further instructions on how to setup Credentials with Open edX, check the `Official Credentials documentation <https://readthedocs.org/projects/edx-credentials/>`__.

Configuration
-------------

Application configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_HOST`` (default: ``"credentials.{{ LMS_HOST }}"``)
- ``CREDENTIALS_LMS_HOST``  (default: ``"myopenedxsite.com"``)
- ``CREDENTIALS_LMS_URL_ROOT`` (default: ``"http://{{ CREDENTIALS_LMS_HOST }}"``)
- ``CREDENTIALS_LMS_URL``  (default: ``"http://{{ CREDENTIALS_LMS_HOST }}"``)
- ``CREDENTIALS_MYSQL_DATABASE`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_USERNAME`` (default: ``"credentials"``)
- ``CREDENTIALS_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``CREDENTIALS_CATALOG_API_URL`` (default: ``"{{ LMS_HOST }}"``)
- ``CREDENTIALS_DOCKER_IMAGE`` (default: ``"{{ DOCKER_REGISTRY }}lpm0073/openedx-credentials:{{ CREDENTIALS_VERSION }}"``)
- ``CREDENTIALS_EXTRA_PIP_REQUIREMENTS`` (default: ``[]``)
- ``CREDENTIALS_PRIVACY_POLICY_URL``  (default: ``"LMS_HOST/pricacy-policy"``)
- ``CREDENTIALS_SECRET_KEY`` (default: ``"CHANGE-ME"``)
- ``CREDENTIALS_SITE_NAME`` (default: ``"LMS_HOST"``)
- ``CREDENTIALS_TOS_URL`` (default: ``"{{ LMS_HOST }}/tos"``)

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

Back end authentication
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

Operations
----------

Using Django Admin
~~~~~~~~~~~~~~~~~~

The credentials user interface will be available at http://credentials.local.overhang.io for a local instance, and at ``CREDENTIALS_HOST`` (by  default: ``http(s)://credentials.<your lms host>``) in production. In order to run commands from the UI login with an admin user at: http://credentials.local.overhang.io/admin/

Funding
-------

.. image:: https://www.academiacentral.org/wp-content/uploads/2019/05/academia-nobeta.png
    :alt: Academia Central
    :target: https://www.academiacentral.org/

This plugin was developed and open sourced to the community thanks to the generous support of `Academia Central <https://www.academiacentral.org/>`_. Thank you!

License
-------

This software is licensed under the terms of the AGPLv3.