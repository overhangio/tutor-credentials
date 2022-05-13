from glob import glob
import os
import pkg_resources

from tutor import hooks as tutor_hooks

from .__about__ import __version__


################# Configuration
config = {
    # Add here your new settings
    "defaults": {
        "VERSION": __version__,
        "API_TIMEOUT": 5,
        "CURRENCY": "USD",
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-credentials:{{ CREDENTIALS_VERSION }}",
        "WORKER_DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-credentials-worker:{{ CREDENTIALS_VERSION }}",
        "EXTRA_PIP_REQUIREMENTS": [],
        "HOST": "credentials.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "credentials",
        "MYSQL_USERNAME": "credentials",
        "OAUTH2_KEY": "credentials",
        "OAUTH2_KEY_DEV": "credentials-dev",
        "OAUTH2_KEY_SSO": "credentials-sso",
        "OAUTH2_KEY_SSO_DEV": "credentials-sso-dev",
    },
    # Add here settings that don't have a reasonable default for all users. For
    # instance: passwords, secret keys, etc.
    "unique": {
        # "SECRET_KEY": "\{\{ 24|random_string \}\}",
    },
    # Danger zone! Add here values to override settings from Tutor core or other plugins.
    "overrides": {
        # "PLATFORM_NAME": "My platform",
    },
}

################# Initialization tasks
tutor_hooks.Filters.COMMANDS_INIT.add_item(
    (
        "lms",
        ("credentials", "tasks", "lms", "init"),
    )
)
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "credentials",
        ("plugins", "credentials", "build", "credentials"),
        "{{ CREDENTIALS_DOCKER_IMAGE }}",
        (),
    )
)

@tutor_hooks.Filters.IMAGES_PULL.add()
@tutor_hooks.Filters.IMAGES_PUSH.add()
def _add_remote_credentials_image_iff_customized(images, user_config):
    """
    Register CREDENTIALS image for pushing & pulling if and only if it has
    been set to something other than the default.

    This is work-around to an upstream issue with CREDENTIALS config. Briefly:
    User config is baked into CREDENTIALS builds, so Tutor cannot host a generic
    pre-built CREDENTIALS image. Howevever, individual Tutor users may want/need to
    build and host their own CREDENTIALS image. So, as a compromise, we tell Tutor
    to push/pull the CREDENTIALS image if the user has customized it to anything
    other than the default image URL.
    """
    image_tag = user_config["CREDENTIALS_DOCKER_IMAGE"]
    if not image_tag.startswith("docker.io/lpm0073/openedx-credentials:"):
        # Image has been customized. Add to list for pulling/pushing.
        images.append(("credentials", image_tag))
    return images


################# You don't really have to bother about what's below this line,
################# except maybe for educational purposes :)

# Plugin templates
tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    pkg_resources.resource_filename("tutorcredentials", "templates")
)
tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("credentials/build", "plugins"),
        ("credentials/apps", "plugins"),
    ],
)
# Load all patches from the "patches" folder
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorcredentials", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))

# Load all configuration entries
tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        (f"CREDENTIALS_{key}", value)
        for key, value in config["defaults"].items()
    ]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        (f"CREDENTIALS_{key}", value)
        for key, value in config["unique"].items()
    ]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(list(config["overrides"].items()))
