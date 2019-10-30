FROM python:3.7-alpine3.9

RUN apk add --update \
  bash \
  gcc \
  musl-dev \
  postgresql-dev \
  libxml2-dev \
  libffi-dev \
  libxslt-dev \
  supervisor \
  && rm /var/cache/apk/*

RUN mkdir -p /opt/text2lex/api
ADD requirements.txt /opt/text2lex/api
WORKDIR /opt/text2lex/api
RUN pip install -r requirements.txt
ADD . /opt/text2lex/api

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]