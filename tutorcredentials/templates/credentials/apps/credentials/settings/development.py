from credentials.settings.devstack import * # pylint: disable=wildcard-import, unused-wildcard-import

{% include "credentials/apps/credentials/settings/partials/common.py" %}

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://{{ LMS_HOST }}:8000"
FAVICON_URL = "http://{{ LMS_HOST }}:8000/favicon.ico"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY }}"

# Disable API caching, which makes it a pain to troubleshoot issues
USE_API_CACHING = False

{{ patch("credentials-settings-development") }}
