from __future__ import annotations

import os
import typing as t
from glob import glob

import importlib_resources
from tutor import hooks as tutor_hooks
from tutor.__about__ import __version_suffix__
from tutormfe.hooks import MFE_APPS, MFE_ATTRS_TYPE

from .__about__ import __version__

# Handle version suffix in main mode, just like tutor core
if __version_suffix__:
    __version__ += "-" + __version_suffix__


########################################
# CONFIGURATION
########################################

config: t.Dict[str, t.Dict[str, t.Any]] = {
    "defaults": {
        "VERSION": __version__,
        "BACKEND_SERVICE_EDX_OAUTH2_KEY": "{{ CREDENTIALS_OAUTH2_KEY }}",
        "DOCKER_IMAGE": "{{ DOCKER_REGISTRY }}overhangio/openedx-credentials:{{ CREDENTIALS_VERSION }}",  # noqa: E501
        "EXTRA_PIP_REQUIREMENTS": [],
        "HOST": "credentials.{{ LMS_HOST }}",
        "MYSQL_DATABASE": "credentials",
        "MYSQL_USERNAME": "credentials",
        "OAUTH2_KEY": "credentials-key",
        "OAUTH2_KEY_DEV": "credentials-key-dev",
        "OAUTH2_KEY_SSO": "credentials-key-sso",
        "OAUTH2_KEY_SSO_DEV": "credentials-key-sso-dev",
        "SOCIAL_AUTH_EDX_OAUTH2_KEY": "credentials-sso-key",
        "THEME_NAME": "edx-theme",
        "REPOSITORY": "https://github.com/openedx/credentials.git",
        "REPOSITORY_VERSION": "{{ OPENEDX_COMMON_VERSION }}",
        "SERVICE_USERNAME": "credentials",
    },
    "unique": {
        "MYSQL_PASSWORD": "{{ 8|random_string }}",
        "SOCIAL_AUTH_EDX_OAUTH2_SECRET": "{{ 16|random_string }}",
        "BACKEND_SERVICE_EDX_OAUTH2_SECRET": "{{ 16|random_string }}",
        "OAUTH2_SECRET": "{{ 16|random_string }}",
        "OAUTH2_SECRET_DEV": "{{ 16|random_string }}",
        "OAUTH2_SECRET_SSO": "{{ 16|random_string }}",
        "OAUTH2_SECRET_SSO_DEV": "{{ 16|random_string }}",
    },
}

tutor_hooks.Filters.CONFIG_DEFAULTS.add_items(
    [(f"CREDENTIALS_{key}", value) for key, value in config.get("defaults", {}).items()]
)
tutor_hooks.Filters.CONFIG_UNIQUE.add_items(
    [(f"CREDENTIALS_{key}", value) for key, value in config.get("unique", {}).items()]
)
tutor_hooks.Filters.CONFIG_OVERRIDES.add_items(
    list(config.get("overrides", {}).items())
)


########################################
# MFEs
########################################


@MFE_APPS.add()  # type: ignore
def _add_learner_record_mfe(
    apps: dict[str, MFE_ATTRS_TYPE],
) -> dict[str, MFE_ATTRS_TYPE]:
    apps.update(
        {
            "learner-record": {
                "repository": "https://github.com/openedx/frontend-app-learner-record.git",
                "port": 1990,
            },
        }
    )
    return apps


########################################
# INITIALIZATION TASKS
########################################

MY_INIT_TASKS = [
    ("mysql", "init"),
    ("lms", "init"),
    ("credentials", "init"),
    ("mysql", "sync_users"),
]

HERE = os.path.abspath(os.path.dirname(__file__))
for service, template_name in MY_INIT_TASKS:
    full_path: str = str(
        importlib_resources.files("tutorcredentials")
        / "templates"
        / "credentials"
        / "tasks"
        / service
        / template_name
    )

    with open(full_path, encoding="utf-8") as init_task_file:
        init_task: str = init_task_file.read()
        tutor_hooks.Filters.CLI_DO_INIT_TASKS.add_item((service, init_task))


########################################
# Credentials Public Host
########################################


@tutor_hooks.Filters.APP_PUBLIC_HOSTS.add()
def _print_credentials_public_hosts(
    hosts: list[str], context_name: t.Literal["local", "dev"]
) -> list[str]:
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
def _mount_credentials_apps(
    mounts: list[tuple[str, str]], path_basename: str
) -> list[tuple[str, str]]:
    if path_basename == REPO_NAME:
        app_name = REPO_NAME
        mounts += [(app_name, "/openedx/credentials")]
    return mounts


# Bind-mount repo at build-time, both for prod and dev images
@tutor_hooks.Filters.IMAGES_BUILD_MOUNTS.add()
def _mount_credentials_on_build(
    mounts: list[tuple[str, str]], host_path: str
) -> list[tuple[str, str]]:
    path_basename = os.path.basename(host_path)
    if path_basename == REPO_NAME:
        app_name = REPO_NAME
        mounts.append((app_name, f"{app_name}-src"))
        mounts.append((f"{app_name}-dev", f"{app_name}-src"))
    return mounts


########################################
# DOCKER IMAGE MANAGEMENT
########################################

tutor_hooks.Filters.IMAGES_BUILD.add_item(
    (
        "credentials",
        ("plugins", "credentials", "build", "credentials"),
        "{{ CREDENTIALS_DOCKER_IMAGE }}",
        (),
    )
)
tutor_hooks.Filters.IMAGES_PULL.add_item(
    (
        "credentials",
        "{{ CREDENTIALS_DOCKER_IMAGE }}",
    )
)
tutor_hooks.Filters.IMAGES_PUSH.add_item(
    (
        "credentials",
        "{{ CREDENTIALS_DOCKER_IMAGE }}",
    )
)


########################################
# TEMPLATE RENDERING
########################################

tutor_hooks.Filters.ENV_TEMPLATE_ROOTS.add_item(
    # Root path for template files, relative to the project root.
    str(importlib_resources.files("tutorcredentials") / "templates")
)

tutor_hooks.Filters.ENV_TEMPLATE_TARGETS.add_items(
    [
        ("credentials/build", "plugins"),
        ("credentials/apps", "plugins"),
    ],
)


########################################
# PATCH LOADING
########################################

for path in glob(str(importlib_resources.files("tutorcredentials") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        tutor_hooks.Filters.ENV_PATCHES.add_item(
            (os.path.basename(path), patch_file.read())
        )
