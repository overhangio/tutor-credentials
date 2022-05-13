import logging.config

from credentials.settings.utils import get_logger_config
from credentials.settings.production import *

{% include "credentials/apps/credentials/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ CREDENTIALS_MFE_HOST }}",
]
CSRF_TRUSTED_ORIGINS = ["{{ CREDENTIALS_MFE_HOST }}"]

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY }}"

# Logging: get rid of local handler
LOGGING = get_logger_config(
    log_dir="/var/log",
    edx_filename="credentials.log",
    dev_env=True,
    debug=False,
    local_loglevel="INFO",
)
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    try:
        logger["handlers"].remove("local")
    except ValueError:
        continue
logging.config.dictConfig(LOGGING)


{{ patch("credentials-settings-production") }}
