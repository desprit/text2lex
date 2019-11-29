FROM python:3.7-slim-buster

RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc supervisor libpq-dev python-dev \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get purge -y --auto-remove

RUN mkdir -p /opt/text2lex/nlp
ADD requirements.txt /opt/text2lex/nlp
WORKDIR /opt/text2lex/nlp
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
ADD . /opt/text2lex/nlp

ADD supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]