from __future__ import annotations

from glob import glob
import os
import pkg_resources
import typing as t

from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__

from .__about__ import __version__

# Handle version suffix in nightly mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__


########################################
# CONFIGURATION
########################################

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair, (setting_name, default_value).
        # Prefix your setting names with 'CREDENTIALS_'.
        ("CREDENTIALS_VERSION", __version__),
        ("CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_PROVIDER_URL", "http://lms:8000/oauth2"),
        ("CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_KEY", "{{ CREDENTIALS_OAUTH2_KEY }}"),
        ("CREDENTIALS_DOCKER_IMAGE", "{{ DOCKER_REGISTRY }}overhangio/openedx-credentials:{{ CREDENTIALS_VERSION }}"),
        ("CREDENTIALS_EXTRA_PIP_REQUIREMENTS", []),
        ("CREDENTIALS_FAVICON_URL", "https://edx-cdn.org/v3/default/favicon.ico"),
        ("CREDENTIALS_HOST", "credentials.{{ LMS_HOST }}"),
        ("CREDENTIALS_LOGO_TRADEMARK_URL", "https://edx-cdn.org/v3/default/logo-trademark.svg"),
        ("CREDENTIALS_LOGO_TRADEMARK_URL_PNG", "https://edx-cdn.org/v3/default/logo-trademark.png"),
        ("CREDENTIALS_LOGO_TRADEMARK_URL_SVG", "https://edx-cdn.org/v3/default/logo-trademark.svg"),
        ("CREDENTIALS_LOGO_URL", ""),
        ("CREDENTIALS_LOGO_URL_PNG", "{{ CREDENTIALS_LOGO_URL }}"),
        ("CREDENTIALS_LOGO_URL_SVG", ""),
        ("CREDENTIALS_LOGO_WHITE_URL", "{{ CREDENTIALS_LOGO_URL }}"),
        ("CREDENTIALS_LOGO_WHITE_URL_PNG", "{{ CREDENTIALS_LOGO_URL }}"),
        ("CREDENTIALS_LOGO_WHITE_URL_SVG", ""),
        ("CREDENTIALS_MYSQL_DATABASE", "credentials"),
        ("CREDENTIALS_MYSQL_USERNAME", "credentials"),
        ("CREDENTIALS_OAUTH2_KEY", "credentials-key"),
        ("CREDENTIALS_OAUTH2_KEY_DEV", "credentials-key-dev"),
        ("CREDENTIALS_OAUTH2_KEY_SSO", "credentials-key-sso"),
        ("CREDENTIALS_OAUTH2_KEY_SSO_DEV", "credentials-key-sso-dev"),
        ("CREDENTIALS_PLATFORM_NAME", "{{ PLATFORM_NAME }}"),
        ("CREDENTIALS_SITE_NAME", "{{ LMS_HOST }}"),
        ("CREDENTIALS_SOCIAL_AUTH_REDIRECT_IS_HTTPS", False),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_ISSUER", "https://{{ LMS_HOST }}"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT", "http://lms:8000"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_KEY", "credentials-sso-key"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL", "{{ LMS_HOST }}/logout"),
        ("CREDENTIALS_THEME_NAME", "edx-theme"),
        ("CREDENTIALS_REPOSITORY", "https://github.com/edx/credentials.git"),
        ("CREDENTIALS_REPOSITORY_VERSION", "{{ OPENEDX_COMMON_VERSION }}"),
    ]
)

tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [
        # Add settings that don't have a reasonable default for all users here.
        # For instance, passwords, secret keys, etc.
        # Each new setting is a pair, (setting_name, unique_generated_value).
        # Prefix your setting names with 'CREDENTIALS_'.
        # For example:
        ("CREDENTIALS_MYSQL_PASSWORD", "{{ 8|random_string }}"),
        ("CREDENTIALS_SOCIAL_AUTH_EDX_OAUTH2_SECRET", "{{ 16|random_string }}"),
        ("CREDENTIALS_BACKEND_SERVICE_EDX_OAUTH2_SECRET", "{{ 16|random_string }}"),
        ("CREDENTIALS_OAUTH2_SECRET", "{{ 16|random_string }}"),
        ("CREDENTIALS_OAUTH2_SECRET_DEV", "{{ 16|random_string }}"),
        ("CREDENTIALS_OAUTH2_SECRET_SSO", "{{ 16|random_string }}"),
        ("CREDENTIALS_OAUTH2_SECRET_SSO_DEV", "{{ 16|random_string }}"),
    ]
)

tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    [
        # Danger zone!
        # Add values to override settings from Tutor core or other plugins here.
        # Each override is a pair, (setting_name, new_value). For example:
        # ("PLATFORM_NAME", "My platform"),
    ]
)


########################################
# INITIALIZATION TASKS
########################################

# To run the script from templates/credentials/tasks/myservice/init, add:
MY_INIT_TASKS = [
    ("mysql", ("templates", "credentials", "tasks", "mysql", "init")),
    ("lms", ("templates", "credentials", "tasks", "lms", "init")),
    ("credentials", ("templates", "credentials", "tasks", "credentials", "init")),
    ("mysql", ("templates", "credentials", "tasks", "mysql", "sync_users")),
]

HERE = os.path.abspath(os.path.dirname(__file__))
for service, template_path in MY_INIT_TASKS:
    full_path: str = os.path.join(HERE, *template_path)

    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
        tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))

########################################
# Credentials Public Host
########################################


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_credentials_public_hosts(hosts: list[str], context_name: t.Literal["local", "dev"]) -> list[str]:
    if context_name == "dev":
        hosts += ["{{ CREDENTIALS_HOST }}:8150"]
    else:
        hosts += ["{{ CREDENTIALS_HOST }}"]
    return hosts


########################################
# Mount Credentials
########################################

REPO_NAME = "credentials"


# Automount /openedx/credentials folder from the container
@tutor_hooks.Filters.COMPOSE_MOUNTS.add()
def _mount_credentials_apps(mounts, path_basename):
    if path_basename == REPO_NAME:
        app_name = REPO_NAME
        mounts += [(app_name, "/openedx/credentials")]
    return mounts


# Bind-mount repo at build-time, both for prod and dev images
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_credentials_on_build(mounts: list[tuple[str, str]], host_path: str) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == REPO_NAME:
        app_name = REPO_NAME
        mounts.append((app_name, f"{app_name}-src"))
        mounts.append((f"{app_name}-dev", f"{app_name}-src"))
    return mounts


########################################
# DOCKER IMAGE MANAGEMENT
########################################

# To build an image with `tutor images build myimage`, add a Dockerfile to templates/credentials/build/myimage and write:
tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "credentials",
        ("plugins", "credentials", "build", "credentials"),
        "{{ CREDENTIALS_DOCKER_IMAGE }}",
        (),
    )
)


# To pull/push an image with `tutor images pull myimage` and `tutor images push myimage`, write:
# tutor_hooks.Filters.IMAGES_PULL.add_item((
#     "myimage",
#     "docker.io/myimage:{{ CREDENTIALS_VERSION }}",
# )
# tutor_hooks.Filters.IMAGES_PUSH.add_item((
#     "myimage",
#     "docker.io/myimage:{{ CREDENTIALS_VERSION }}",
# )


########################################
# TEMPLATE RENDERING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_items(
    # Root paths for template files, relative to the project root.
    [
        pkg_resources.resource_filename("tutorcredentials", "templates"),
    ]
)

tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    # For each pair (source_path, destination_path):
    # templates at ``source_path`` (relative to your ENV_TEMPLATE_ROOTS) will be
    # rendered to ``destination_path`` (relative to your Tutor environment).
    [
        ("credentials/build", "plugins"),
        ("credentials/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorcredentials/patches,
# apply a patch based on the file's name and contents.
for path in glob(
    os.path.join(
        pkg_resources.resource_filename("tutorcredentials", "patches"),
        "*",
    )
):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
