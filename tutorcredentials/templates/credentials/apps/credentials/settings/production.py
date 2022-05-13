import platform
from sys import stdout as sys_stdout
from credentials.settings.production import * # pylint: disable=wildcard-import, unused-wildcard-import

{% include "credentials/apps/credentials/settings/partials/common.py" %}

CORS_ORIGIN_WHITELIST = list(CORS_ORIGIN_WHITELIST) + [
    "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ CREDENTIALS_MFE_HOST }}",
]
CSRF_TRUSTED_ORIGINS = ["{{ CREDENTIALS_MFE_HOST }}"]

SOCIAL_AUTH_EDX_OAUTH2_PUBLIC_URL_ROOT = "{% if ENABLE_HTTPS %}https{% else %}http{% endif %}://{{ LMS_HOST }}"

BACKEND_SERVICE_EDX_OAUTH2_KEY = "{{ CREDENTIALS_OAUTH2_KEY }}"

def get_docker_logger_config(log_dir='/var/tmp',
                             logging_env="no_env",
                             edx_filename="edx.log",
                             dev_env=False,
                             debug=False,
                             service_variant='credentials'):
    """
    Return the appropriate logging config dictionary. You should assign the
    result of this to the LOGGING var in your settings.
    """

    hostname = platform.node().split(".")[0]
    syslog_format = (
        "[service_variant={service_variant}]"
        "[%(name)s][env:{logging_env}] %(levelname)s "
        "[{hostname}  %(process)d] [%(filename)s:%(lineno)d] "
        "- %(message)s"
    ).format(
        service_variant=service_variant,
        logging_env=logging_env, hostname=hostname
    )

    handlers = ['console']

    logger_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s %(levelname)s %(process)d '
                          '[%(name)s] %(filename)s:%(lineno)d - %(message)s',
            },
            'syslog_format': {'format': syslog_format},
            'raw': {'format': '%(message)s'},
        },
        'handlers': {
            'console': {
                'level': 'DEBUG' if debug else 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'standard',
                'stream': sys_stdout,
            },
        },
        'loggers': {
            'django': {
                'handlers': handlers,
                'propagate': True,
                'level': 'INFO'
            },
            'requests': {
                'handlers': handlers,
                'propagate': True,
                'level': 'WARNING'
            },
            'factory': {
                'handlers': handlers,
                'propagate': True,
                'level': 'WARNING'
            },
            'django.request': {
                'handlers': handlers,
                'propagate': True,
                'level': 'WARNING'
            },
            '': {
                'handlers': handlers,
                'level': 'DEBUG',
                'propagate': False
            },
        }
    }

    return logger_config

LOGGING = get_docker_logger_config()

{{ patch("credentials-settings-production") }}
