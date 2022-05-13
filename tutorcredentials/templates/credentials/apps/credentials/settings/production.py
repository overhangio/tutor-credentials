from credentials.settings.production import * # pylint: disable=wildcard-import, unused-wildcard-import

{% include "credentials/apps/credentials/settings/partials/common.py" %}

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY }}"

# Get rid of local logger
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    logger["handlers"].remove("local")

{{ patch("credentials-settings-production") }}
