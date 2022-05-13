FROM docker.io/ubuntu:20.04

RUN apt update && \
  apt install -y curl git-core language-pack-en libmysqlclient-dev libssl-dev python3 python3-pip python3-venv

ARG APP_USER_ID=1000
RUN useradd --home-dir /openedx --create-home --shell /bin/bash --uid ${APP_USER_ID} app
USER ${APP_USER_ID}

# Create python venv
RUN python3 -m venv /openedx/venv/
ENV PATH "/openedx/venv/bin:$PATH"
RUN pip install setuptools==44.1.0 pip==20.3.4

# Create Node environment
RUN pip install nodeenv
ENV NOVE_ENV=/openedx/nodeenv
RUN nodeenv $NODE_ENV --node=16.14.0 --prebuilt
ENV PATH="$NODE_ENV/bin:$PATH"

# nodejs requirements (aka: "make requirements.js")
ARG NPM_REGISTRY=https://registry.npmjs.org/
RUN npm install -g npm@8.5.3 --verbose --registry=$NPM_REGIST RY

RUN locale-gen en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV DJANGO_SETTINGS_MODULE credentials.settings.production


# Install credentials
ARG CREDENTIALS_REPOSITORY=https://github.com/edx/credentials.git
ARG CREDENTIALS_VERSION="open-release/maple.master"
RUN mkdir -p /openedx/credentials && \
    git clone $CREDENTIALS_REPOSITORY --branch $CREDENTIALS_VERSION --depth 1 /openedx/credentials
WORKDIR /openedx/credentials


# python requirements
RUN pip install -r requirements/pip_tools.txt
RUN pip install -r requirements.txt
RUN pip install uwsgi==2.0.19.1

# Install private requirements
COPY --chown=app:app ./requirements/ /openedx/requirements
RUN cd /openedx/requirements/ \
  && touch ./private.txt \
  && pip install -r ./private.txt

{% for extra_requirement in CREDENTIALS_EXTRA_PIP_REQUIREMENTS %}RUN pip install {{ extra_requirement }}
{% endfor %}

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV CREDENTIALS_CFG /openedx/config.yml

EXPOSE 8000
CMD uwsgi \
    --static-map /static=/openedx/credentials/assets \
    --static-map /media=/openedx/credentials/course_credentials/media \
    --http 0.0.0.0:8000 \
    --thunder-lock \
    --single-interpreter \
    --enable-threads \
    --processes=2 \
    --buffer-size=8192 \
    --wsgi-file credentials/wsgi.py
