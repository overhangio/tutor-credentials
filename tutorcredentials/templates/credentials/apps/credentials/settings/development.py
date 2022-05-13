from ..devstack import *

{% include "credentials/apps/credentials/settings/partials/common.py" %}


SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://{{ LMS_HOST }}:8000"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY_DEV }}"

{{ patch("credentials-settings-development") }}
