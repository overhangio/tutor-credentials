from credentials.settings.utils import get_logger_config

# Get rid of local logger
LOGGING = get_logger_config(debug=True, dev_env=True, local_loglevel="INFO")
#del LOGGING["handlers"]["local"]


{{ patch("credentials-settings-common") }}