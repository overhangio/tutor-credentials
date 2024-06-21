# syntax=docker/dockerfile:1
###### Minimal image with base system requirements for most stages
FROM docker.io/ubuntu:20.04 AS minimal

ENV DEBIAN_FRONTEND=noninteractive
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    apt update && \
    apt install -y build-essential curl git language-pack-en gettext

ENV LC_ALL=en_US.UTF-8
{{ patch("credentials-dockerfile-minimal") }}


###### Install python with pyenv in /opt/pyenv and create virtualenv in /openedx/venv
FROM minimal AS python
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked apt update && \
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git

# Install pyenv
# https://www.python.org/downloads/
# https://github.com/pyenv/pyenv/releases
ARG PYTHON_VERSION=3.11.9
ENV PYENV_ROOT=/opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.4.0 --depth 1

# Install Python
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv

###### Checkout credentials
FROM minimal AS code
ARG CREDENTIALS_REPOSITORY="{{ CREDENTIALS_REPOSITORY }}"
ARG CREDENTIALS_VERSION="{{ CREDENTIALS_REPOSITORY_VERSION }}"
RUN mkdir -p /openedx/credentials && \
    git clone $CREDENTIALS_REPOSITORY --branch $CREDENTIALS_VERSION --depth 1 /openedx/credentials
WORKDIR /openedx/credentials

{{ patch("credentials-dockerfile-post-git-checkout") }}

###### Install python requirements in virtualenv
FROM python AS python-requirements
ENV PATH=/openedx/venv/bin:${PATH}
ENV VIRTUAL_ENV=/openedx/venv/

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked apt update \
    && apt install -y software-properties-common libmysqlclient-dev libxmlsec1-dev

# Note that this means that we need to reinstall all requirements whenever there is a
# change in credentials, which sucks. But there is no obvious alternative, as we need
# to install some packages from credentials.
COPY --from=code /openedx/credentials /openedx/credentials
WORKDIR /openedx/credentials

# Install the right version of pip/setuptools
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # https://pypi.org/project/setuptools/
    # https://pypi.org/project/pip/
    # https://pypi.org/project/wheel/
    setuptools==69.1.1 pip==24.0 wheel==0.43.0

# Install base requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install -r requirements/production.txt

# Install extra requirements
RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install \
    # Use redis as a django cache https://pypi.org/project/django-redis/
    django-redis==5.4.0 \
    # uwsgi server https://pypi.org/project/uWSGI/
    uwsgi==2.0.24

{{ patch("credentials-dockerfile-post-python-requirements") }}

{% for extra_requirement in CREDENTIALS_EXTRA_PIP_REQUIREMENTS %}RUN --mount=type=cache,target=/openedx/.cache/pip,sharing=shared pip install '{{ extra_requirement }}'
{% endfor %}

###### Install nodejs with nodeenv in /openedx/nodeenv
FROM python AS nodejs-requirements
ENV PATH=/openedx/nodeenv/bin:/openedx/venv/bin:${PATH}

# Install nodeenv with the version provided by credentials
# https://github.com/ekalinin/nodeenv/releases
RUN pip install nodeenv==1.8.0
RUN nodeenv /openedx/nodeenv --node=16.14.2 --prebuilt

# Install nodejs requirements
ARG NPM_REGISTRY='{{ NPM_REGISTRY }}'
COPY --from=code /openedx/credentials/package.json /openedx/credentials/package.json
WORKDIR /openedx/credentials
RUN --mount=type=cache,target=/openedx/.npm/,sharing=shared npm install --verbose --registry=$NPM_REGISTRY

###### Production image with system and python requirements
FROM minimal AS production

# Install system requirements
RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked apt update \
    && apt install -y libxml2 libmysqlclient-dev mime-support

# From then on, run as unprivileged "app" user
ARG APP_USER_ID=1000
RUN if [ "$APP_USER_ID" = 0 ]; then echo "app user may not be root" && false; fi
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# change file ownership to the new app user
COPY --chown=app:app --from=code /openedx/credentials /openedx/credentials
COPY --chown=app:app --from=python /opt/pyenv /opt/pyenv
COPY --chown=app:app --from=python-requirements /openedx/venv /openedx/venv
COPY --chown=app:app --from=nodejs-requirements /openedx/nodeenv /openedx/nodeenv
COPY --chown=app:app --from=nodejs-requirements /openedx/credentials/node_modules /openedx/node_modules

# Symlink node_modules such that we can bind-mount the credentials repository
RUN ln -s /openedx/node_modules /openedx/credentials/node_modules

ENV PATH=/openedx/venv/bin:./node_modules/.bin:/openedx/nodeenv/bin:${PATH}
ENV VIRTUAL_ENV=/openedx/venv/
WORKDIR /openedx/credentials

RUN atlas pull --repository="{{ ATLAS_REPOSITORY }}" --branch="{{ ATLAS_REVISION }}" {{ ATLAS_OPTIONS }} translations/credentials/credentials/conf/locale:credentials/conf/locale
RUN python manage.py compilemessages

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CREDENTIALS_CFG=/openedx/config.yml

{{ patch("credentials-dockerfile-pre-assets") }}

# Collect static assets
COPY --chown=app:app assets.py ./credentials/settings/assets.py
ENV DJANGO_SETTINGS_MODULE=credentials.settings.assets
RUN python3 manage.py compilejsi18n
RUN node_modules/.bin/webpack --config webpack.config.js
RUN python3 manage.py collectstatic --noinput

ENV DJANGO_SETTINGS_MODULE=credentials.settings.tutor.production

# Create a data directory, which might be used (or not)
RUN mkdir /openedx/data

{{ patch("credentials-dockerfile") }}

EXPOSE 8000

###### Final image with production cmd
FROM production AS final

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
