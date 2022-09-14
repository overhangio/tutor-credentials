FROM docker.io/ubuntu:20.04 as minimal
LABEL maintainer="Lawrence McDaniel <lpm0073@gmail.com>"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && \
    apt install -y build-essential curl git language-pack-en

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
{{ patch("credentials-dockerfile-minimal") }}


###### Install python with pyenv in /opt/pyenv and create virtualenv in /openedx/venv
FROM minimal as python
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN apt update && \
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python-openssl git
ARG PYTHON_VERSION=3.8.12
ENV PYENV_ROOT /opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.2.2 --depth 1
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /openedx/venv

###### Install Dockerize to wait for mysql DB availability
FROM minimal as dockerize
# https://github.com/powerman/dockerize/releases
ARG DOCKERIZE_VERSION=v0.16.0
RUN dockerize_url="https://github.com/powerman/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-$(uname -m | sed 's@aarch@arm@')" \
    && echo "Downloading dockerize from $dockerize_url" \
    && curl --fail --location --output /usr/local/bin/dockerize $dockerize_url \
    && chmod a+x /usr/local/bin/dockerize

###### Checkout credentials
FROM minimal as code
ARG CREDENTIALS_REPOSITORY=https://github.com/edx/credentials.git
ARG CREDENTIALS_VERSION="open-release/nutmeg.master"
RUN mkdir -p /openedx/credentials && \
    git clone $CREDENTIALS_REPOSITORY --branch $CREDENTIALS_VERSION --depth 1 /openedx/credentials
WORKDIR /openedx/credentials

{{ patch("credentials-dockerfile-post-git-checkout") }}

###### Download extra locales to /openedx/locale/contrib/locale
# mcdaniel: including these just in case there are implied dependencies
# on emitted credential data, which would be platform specific obviously.
FROM minimal as locales
ARG OPENEDX_I18N_VERSION={{ OPENEDX_COMMON_VERSION }}
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

RUN apt update && apt install -y software-properties-common libmysqlclient-dev libxmlsec1-dev libgeos-dev

# Note that this means that we need to reinstall all requirements whenever there is a
# change in credentials, which sucks. But there is no obvious alternative, as we need
# to install some packages from credentials.
COPY --from=code /openedx/credentials /openedx/credentials
WORKDIR /openedx/credentials

# Install the right version of pip/setuptools
RUN pip install setuptools==44.1.0 pip==20.0.2 wheel==0.34.2

# Install base requirements
RUN pip install -r requirements/pip_tools.txt
RUN pip install -r requirements.txt

# Install django-redis for using redis as a django cache
RUN pip install django-redis==4.12.1

# Install uwsgi
RUN pip install uwsgi==2.0.20

{{ patch("credentials-dockerfile-post-python-requirements") }}

COPY ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in CREDENTIALS_EXTRA_PIP_REQUIREMENTS %}RUN pip install {{ extra_requirement }}
{% endfor %}

###### Install nodejs with nodeenv in /openedx/nodeenv
FROM python as nodejs-requirements
ENV PATH /openedx/nodeenv/bin:/openedx/venv/bin:${PATH}

# Install nodeenv with the version provided by credentials
RUN pip install nodeenv==1.6.0
RUN nodeenv /openedx/nodeenv --node=12.13.0 --prebuilt

# Install nodejs requirements
ARG NPM_REGISTRY={{ NPM_REGISTRY }}
COPY --from=code /openedx/credentials/package.json /openedx/credentials/package.json
WORKDIR /openedx/credentials
RUN npm install --verbose --registry=$NPM_REGISTRY

###### Production image with system and python requirements
FROM minimal as production

# Install system requirements
RUN apt update && \
    apt install -y gettext gfortran graphviz graphviz-dev libffi-dev libfreetype6-dev libgeos-dev libjpeg8-dev liblapack-dev libmysqlclient-dev libpng-dev libsqlite3-dev libxmlsec1-dev lynx ntp pkg-config rdfind && \
    rm -rf /var/lib/apt/lists/*

# From then on, run as unprivileged "app" user
ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

#
COPY --from=dockerize /usr/local/bin/dockerize /usr/local/bin/dockerize
COPY --chown=app:app --from=code /openedx/credentials /openedx/credentials
COPY --chown=app:app --from=locales /openedx/locale /openedx/locale
COPY --chown=app:app --from=python /opt/pyenv /opt/pyenv
COPY --chown=app:app --from=python-requirements /openedx/venv /openedx/venv
COPY --chown=app:app --from=python-requirements /openedx/requirements /openedx/requirements
COPY --chown=app:app --from=nodejs-requirements /openedx/nodeenv /openedx/nodeenv
COPY --chown=app:app --from=nodejs-requirements /openedx/credentials/node_modules /openedx/credentials/node_modules

ENV PATH /openedx/venv/bin:./node_modules/.bin:/openedx/nodeenv/bin:${PATH}
ENV VIRTUAL_ENV /openedx/venv/
WORKDIR /openedx/credentials

# Re-install local requirements, otherwise egg-info folders are missing
RUN pip install -r requirements/production.in

# mcdaniel: this breaks. no idea if we really need it.
# -----------------------------------------------------------------------------
# Copy user-specific locales to /openedx/locale/user/locale and compile them
# RUN mkdir /openedx/locale/user
# COPY --chown=app:app ./locale/ /openedx/locale/user/locale/
# RUN cd /openedx/locale/user && \
#     django-admin compilemessages -v1
# -----------------------------------------------------------------------------

{{ patch("credentials-dockerfile-pre-assets") }}

# Compile i18n strings: in some cases, js locales are not properly compiled out of the box
# and we need to do a pass ourselves. Also, we need to compile the djangojs.js files for
# the downloaded locales.
RUN ./manage.py compilejsi18n --settings=tutor.production
RUN python manage.py collectstatic --noinput --settings=tutor.production

# Create a data directory, which might be used (or not)
RUN mkdir /openedx/data

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CREDENTIALS_CFG /openedx/config.yml

ENV DJANGO_SETTINGS_MODULE credentials.settings.tutor.production

{{ patch("credentials-dockerfile") }}

EXPOSE 8000

###### Final image with production cmd
FROM production as final

CMD uwsgi \
    --static-map /static=/openedx/credentials/assets \
    --static-map /media=/openedx/credentials/course_credentials/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=${UWSGI_WORKERS:-2} \
    --buffer-size=8192 \
    --wsgi-file credentials/wsgi.py
