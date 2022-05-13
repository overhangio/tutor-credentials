from credentials.settings.utils import get_logger_config

# reconfigure logging and Get rid of local logger
LOGGING = get_logger_config(debug=False, dev_env=True, local_loglevel="INFO")
LOGGING["handlers"].pop("local")
for logger in LOGGING["loggers"].values():
    logger["handlers"].remove("local")


{{ patch("credentials-settings-common") }}