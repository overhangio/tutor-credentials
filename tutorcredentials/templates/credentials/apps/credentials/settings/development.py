from credentials.settings.devstack import * # pylint: disable=wildcard-import, unused-wildcard-import

{% include "credentials/apps/credentials/settings/partials/common.py" %}

FAVICON_URL = "http://{{ LMS_HOST }}:8000/favicon.ico"

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "http://{{ MFE_HOST }}:{{ get_mfe('learner-record')["port"] }}",
]
CSRF_TRUSTED_ORIGINS = ["http://{{ MFE_HOST }}:{{ get_mfe('learner-record')["port"] }}"]

LEARNER_RECORD_MFE_RECORDS_PAGE_URL = "http://{{ MFE_HOST }}:{{ get_mfe('learner-record')["port"] }}/learner-record/"

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "http://{{ LMS_HOST }}:8000"
SOCIAL_AUTH_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY_SSO_DEV }}"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "{{ CREDENTIALS_OAUTH2_SECRET_SSO_DEV }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY }}"

# Disable API caching, which makes it a pain to troubleshoot issues
USE_API_CACHING = False

{{ patch("credentials-settings-development") }}
