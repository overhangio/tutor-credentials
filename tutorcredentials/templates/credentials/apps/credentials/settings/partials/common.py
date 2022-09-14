import json
from credentials.settings.utils import get_logger_config

SECRET_KEY = "{{ OPENEDX_SECRET_KEY }}"
ALLOWED_HOSTS = [
    "{{ CREDENTIALS_HOST }}.{{ OPENEDX_LMS_BASE }}",
    "CREDENTIALS",
]
PLATFORM_NAME = "{{ PLATFORM_NAME }}"
PROTOCOL = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}"

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = []

{% set jwt_rsa_key = rsa_import_key(JWT_RSA_PRIVATE_KEY) %}
JWT_AUTH["JWT_ISSUER"] = "{{ JWT_COMMON_ISSUER }}"
JWT_AUTH["JWT_AUDIENCE"] = "{{ JWT_COMMON_AUDIENCE }}"
JWT_AUTH["JWT_SECRET_KEY"] = "{{ JWT_COMMON_SECRET_KEY }}"
JWT_AUTH["JWT_PUBLIC_SIGNING_JWK_SET"] = json.dumps(
    {
        "keys": [
            {
                "kid": "openedx",
                "kty": "RSA",
                "e": "{{ jwt_rsa_key.e|long_to_base64 }}",
                "n": "{{ jwt_rsa_key.n|long_to_base64 }}",
            }
        ]
    }
)
JWT_AUTH["JWT_ISSUERS"] = [
    {
        "ISSUER": "{{ JWT_COMMON_ISSUER }}",
        "AUDIENCE": "{{ JWT_COMMON_AUDIENCE }}",
        "SECRET_KEY": "{{ OPENEDX_SECRET_KEY }}"
    }
]

LOGO_TRADEMARK_URL = "https://edx-cdn.org/v3/default/logo-trademark.svg"
LOGO_TRADEMARK_URL_PNG = "https://edx-cdn.org/v3/default/logo-trademark.png"
LOGO_TRADEMARK_URL_SVG = "https://edx-cdn.org/v3/default/logo-trademark.svg"
LOGO_URL = "https://edx-cdn.org/v3/default/logo.svg"
LOGO_URL_PNG = "https://edx-cdn.org/v3/default/logo.png"
LOGO_URL_SVG = "https://edx-cdn.org/v3/default/logo.svg"
LOGO_WHITE_URL = "https://edx-cdn.org/v3/default/logo-white.svg"
LOGO_WHITE_URL_PNG = "https://edx-cdn.org/v3/default/logo-white.png"
LOGO_WHITE_URL_SVG = "https://edx-cdn.org/v3/default/logo-white.svg"
FAVICON_URL = "https://edx-cdn.org/v3/default/favicon.ico"

SOCIAL_AUTH_REDIRECT_IS_HTTPS = {% if ENABLE_HTTPS %}True{% else %}False{% endif %}
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = "http://lms:8000"

SOCIAL_AUTH_EDX_OAUTH2_KEY = "credentials-sso-key"
SOCIAL_AUTH_EDX_OAUTH2_SECRET = "credentials-sso-secret"
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = SOCIAL_AUTH_EDX_OAUTH2_ISSUER + "/logout"
BACKEND_SERVICE_EDX_OAUTH2_KEY = "credentials-backend-service-key"
BACKEND_SERVICE_EDX_OAUTH2_SECRET = "{{ CREDENTIALS_OAUTH2_SECRET }}"
BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL = "http://lms:8000/oauth2"

EDX_DRF_EXTENSIONS = {
    'OAUTH2_USER_INFO_URL': '{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}/oauth2/user_info',
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "{{ CREDENTIALS_MYSQL_DATABASE }}",
        "USER": "{{ CREDENTIALS_MYSQL_USERNAME }}",
        "PASSWORD": "{{ CREDENTIALS_MYSQL_PASSWORD }}",
        "HOST": "{{ MYSQL_HOST }}",
        "PORT": "{{ MYSQL_PORT }}",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "{{ SMTP_HOST }}"
EMAIL_PORT = "{{ SMTP_PORT }}"
EMAIL_HOST_USER = "{{ SMTP_USERNAME }}"
EMAIL_HOST_PASSWORD = "{{ SMTP_PASSWORD }}"
EMAIL_USE_TLS = {{SMTP_USE_TLS}}

#USE_LEARNER_RECORD_MFE = False
#LEARNER_RECORD_MFE_RECORDS_PAGE_URL = ""

# reconfigure logging and Get rid of local logger
LOGGING = get_logger_config(debug=False, dev_env=True, local_loglevel="INFO")
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    if "local" in logger["handlers"]:
        logger["handlers"].remove("local")

{{ patch("credentials-settings-common") }}
