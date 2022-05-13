from ..devstack import *

{% include "credentials/apps/credentials/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "http://{{ MFE_HOST }}:{{ CREDENTIALS_MFE_APP['port'] }}",
]
CSRF_TRUSTED_ORIGINS = ["{{ MFE_HOST }}:{{ CREDENTIALS_MFE_APP['port'] }}"]

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://{{ LMS_HOST }}:8000"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY_DEV }}"

{{ patch("credentials-settings-development") }}
