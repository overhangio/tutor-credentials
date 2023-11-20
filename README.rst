Credentials plugin for `Tutor <https://docs.tutor.edly.io>`__
===================================================================================

This is a plugin for `Tutor <https://docs.tutor.edly.io>`_ that integrates the `Credentials <https://github.com/openedx/credentials/>`__ application in an Open edX platform.
Credentials application supports course and program certificates. This plugin offers an admin panel where user can do configurations for the certificates of his course and program.

Note that user will have to create the course/program using `Discovery plugin <https://github.com/overhangio/tutor-discovery>`__. Then Credentials plugin will be used for certificates configurations.

.. image:: https://github.com/overhangio/tutor-credentials/blob/main/doc/django-admin-screen-shot.png
    :alt: Django Admin

Installation
------------

::

    pip install https://github.com/overhangio/tutor-credentials.git

Note that this plugin is compatible with `Kubernetes integration <http://docs.tutor.edly.io/k8s.html>`__.


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

Learner Record UI
-----------------

.. image:: https://github.com/overhangio/tutor-credentials/blob/main/doc/learner-record.png
    :alt: Learner Record MFE screenshot

This plugin installs and enables the `Learner Record MFE <https://github.com/openedx/frontend-app-learner-record>`__ by default.  It contains views for a learners current status in a program, their current grade, and the ability to share any earned credentials either publically or with institutions.

The learner can access the Learner Record UI from their profile page by clicking the "View My Records" button.

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
- ``CREDENTIALS_REPOSITORY`` (default: ``"https://github.com/openedx/credentials.git"``)
- ``CREDENTIALS_REPOSITORY_VERSION`` (default: ``"{{ OPENEDX_COMMON_VERSION }}"``)

Marketing & Theming
~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_THEME_NAME`` (default: ``"edx-theme"``)

Backend authentication
~~~~~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_KEY`` (default: ``"credentials-backend-service-key"``)
- ``CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_SECRET`` (default: ``"{{ CREDENTIALS_OAUTH2_SECRET }}"``)
- ``CREDENTIALS_OAUTH2_KEY``  (default: ``credentials-backend-service-key"``)
- ``CREDENTIALS_OAUTH2_SECRET`` (default: ``"CHANGE-ME"``)

Application Third party authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_KEY`` (default: ``"credentials-sso-key"``)
- ``CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_SECRET`` (default: ``"credentials-sso-secret"``)

Learner Record UI configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Learner Record is configurable dynamically via runtime configuration.  To change any of the variables below, go to your LMS's Django admin Site Configuration page (for instance, http://local.overhang.io/admin/site_configuration/siteconfiguration/) and add or modify corresponding JSON dict entries in the appropriate site:

- ``SUPPORT_URL_LEARNER_RECORDS`` (default: ``""``): the URL the learner is taken to when clicking the "read more in our records help area" link.

Funding
-------

.. image:: https://www.academiacentral.org/wp-content/uploads/2019/05/academia-nobeta.png
    :alt: Academia Central
    :target: https://www.academiacentral.org/

This plugin was initially developed and open sourced to the community thanks to the generous support of `Academia Central <https://www.academiacentral.org/>`_. Thank you!

Troubleshooting
---------------

This Tutor plugin is maintained by Muhammad Faraz Maqsood from `Edly <https://edly.io/>`__. Community support is available from the official `Open edX forum <https://discuss.openedx.org>`__. Do you need help with this plugin? See the `troubleshooting <https://docs.tutor.edly.io/troubleshooting.html>`__ section from the Tutor documentation.

License
-------

This software is licensed under the terms of the AGPLv3.
