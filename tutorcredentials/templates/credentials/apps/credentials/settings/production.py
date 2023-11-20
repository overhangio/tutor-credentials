from credentials.settings.production import * # pylint: disable=wildcard-import, unused-wildcard-import

{% include "credentials/apps/credentials/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}",
]
CSRF_TRUSTED_ORIGINS = ["{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}"]

LEARNER_RECORD_MFE_RECORDS_PAGE_URL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ MFE_HOST }}/learner-record/"

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY_SSO }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ CREDENTIALS_OAUTH2_SECRET_SSO }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY }}"

{{ patch("credentials-settings-production") }}
