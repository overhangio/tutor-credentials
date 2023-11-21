{% if is_buildkit_enabled() %}# syntax=docker/dockerfile:1.4{% endif %}
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 as minimal
LABEL maintainer="Lawrence McDaniel <lpm0073@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked{% endif %} \
    apt update && \
    apt install -y build-essential curl git language-pack-en

ENV LC_ALL en_US.UTF-8
{{ patch("credentials-dockerfile-minimal") }}


###### Install python with pyenv in /opt/pyenv and create virtualenv in /openedx/venv
FROM minimal as python
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked {% endif %}apt update && \
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Install pyenv
# https://www.python.org/downloads/
# https://github.com/pyenv/pyenv/releases
ARG PYTHON_VERSION=3.8.15
ENV PYENV_ROOT /opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.3.17 --depth 1

# Install Python
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv

###### Checkout credentials
FROM minimal as code
ARG CREDENTIALS_REPOSITORY="{{ CREDENTIALS_REPOSITORY }}"
ARG CREDENTIALS_VERSION="{{ CREDENTIALS_REPOSITORY_VERSION }}"
RUN mkdir -p /openedx/credentials && \
    git clone $CREDENTIALS_REPOSITORY --branch $CREDENTIALS_VERSION --depth 1 /openedx/credentials
WORKDIR /openedx/credentials

{{ patch("credentials-dockerfile-post-git-checkout") }}

###### Download extra locales to /openedx/locale/contrib/locale
# mcdaniel: including these just in case there are implied dependencies
# on emitted credential data, which would be platform specific obviously.
FROM minimal as locales
ARG OPENEDX_I18N_VERSION="{{ OPENEDX_COMMON_VERSION }}"
RUN cd /tmp \
    && curl -L -o openedx-i18n.tar.gz https://github.com/openedx/openedx-i18n/archive/$OPENEDX_I18N_VERSION.tar.gz \
    && tar xzf /tmp/openedx-i18n.tar.gz \
    && mkdir -p /openedx/locale/contrib \
    && mv openedx-i18n-*/edx-platform/locale /openedx/locale/contrib \
    && rm -rf openedx-i18n*

###### Install python requirements in virtualenv
FROM python as python-requirements
ENV PATH /openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV /openedx/venv/

RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked {% endif %}apt update \
    && apt install -y software-properties-common libmysqlclient-dev libxmlsec1-dev libgeos-dev

# Note that this means that we need to reinstall all requirements whenever there is a
# change in credentials, which sucks. But there is no obvious alternative, as we need
# to install some packages from credentials.
COPY --from=code /openedx/credentials /openedx/credentials
WORKDIR /openedx/credentials

# Install the right version of pip/setuptools
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==67.7.2 pip==23.1.2. wheel==0.40.0

# Install base requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install -r requirements/pip_tools.txt
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install -r requirements.txt

# Install extra requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install \
    # Use redis as a django cache https://pypi.org/project/django-redis/
    django-redis==5.2.0 \
    # uwsgi server https://pypi.org/project/uWSGI/
    uwsgi==2.0.21

{{ patch("credentials-dockerfile-post-python-requirements") }}

# Install private requirements: this is useful for installing custom xblocks.
COPY ./requirements/ /openedx/requirements
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in CREDENTIALS_EXTRA_PIP_REQUIREMENTS %}RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.cache/pip,sharing=shared {% endif %}pip install '{{ extra_requirement }}'
{% endfor %}

###### Install nodejs with nodeenv in /openedx/nodeenv
FROM python as nodejs-requirements
ENV PATH /openedx/nodeenv/bin:/openedx/venv/bin:${PATH}

# Install nodeenv with the version provided by credentials
# https://github.com/ekalinin/nodeenv/releases
RUN pip install nodeenv==1.8.0
RUN nodeenv /openedx/nodeenv --node=16.14.0 --prebuilt

# Install nodejs requirements
ARG NPM_REGISTRY='{{ NPM_REGISTRY }}'
COPY --from=code /openedx/credentials/package.json /openedx/credentials/package.json
WORKDIR /openedx/credentials
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/openedx/.npm/,sharing=shared {% endif %}npm install --verbose --registry=$NPM_REGISTRY

###### Production image with system and python requirements
FROM minimal as production

# Install system requirements
# mcdaniel: these are the edx-platform system requirements.
# TO DO: remove any packages that are not needed for Credentials.
RUN {% if is_buildkit_enabled() %}--mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked {% endif %}apt update \
    && apt install -y gettext gfortran graphviz graphviz-dev libffi-dev libfreetype6-dev libgeos-dev libjpeg8-dev liblapack-dev libmysqlclient-dev libpng-dev libsqlite3-dev libxmlsec1-dev lynx mysql-client ntp pkg-config rdfind

# From then on, run as unprivileged "app" user
ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# change file ownership to the new app user
COPY --chown=app:app --from=code /openedx/credentials /openedx/credentials
COPY --chown=app:app --from=locales /openedx/locale /openedx/locale
COPY --chown=app:app --from=python /opt/pyenv /opt/pyenv
COPY --chown=app:app --from=python-requirements /openedx/venv /openedx/venv
COPY --chown=app:app --from=python-requirements /openedx/requirements /openedx/requirements
COPY --chown=app:app --from=nodejs-requirements /openedx/nodeenv /openedx/nodeenv
COPY --chown=app:app --from=nodejs-requirements /openedx/credentials/node_modules /openedx/node_modules

# Symlink node_modules such that we can bind-mount the credentials repository
RUN ln -s /openedx/node_modules /openedx/credentials/node_modules

ENV PATH /openedx/venv/bin:./node_modules/.bin:/openedx/nodeenv/bin:${PATH}
ENV VIRTUAL_ENV /openedx/venv/
WORKDIR /openedx/credentials

# Re-install local requirements, otherwise egg-info folders are missing
RUN pip install -r requirements/production.in

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CREDENTIALS_CFG /openedx/config.yml

{{ patch("credentials-dockerfile-pre-assets") }}

# Collect static assets
COPY --chown=app:app assets.py ./credentials/settings/assets.py
ENV DJANGO_SETTINGS_MODULE credentials.settings.assets
RUN python3 manage.py compilejsi18n
RUN node_modules/.bin/webpack --config webpack.config.js
RUN python3 manage.py collectstatic --noinput

ENV DJANGO_SETTINGS_MODULE credentials.settings.tutor.production

# Create a data directory, which might be used (or not)
RUN mkdir /openedx/data

{{ patch("credentials-dockerfile") }}

EXPOSE 8000

###### Final image with production cmd
FROM production as final

CMD uwsgi \
    --static-map /static=/openedx/credentials/credentials/assets \
    --static-map /media=/openedx/credentials/credentials/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=${UWSGI_WORKERS:-2} \
    --buffer-size=8192 \
    --wsgi-file credentials/wsgi.py
