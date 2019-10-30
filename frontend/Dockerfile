FROM node:alpine as dev-stage

RUN apk update \
  && apk add --update alpine-sdk \
  && apk add --no-cache bash git openssh vim musl-dev \
  && apk del alpine-sdk \
  && rm -rf /tmp/* /var/cache/apk/* *.tar.gz ~/.npm \
  && npm cache verify \
  && sed -i -e "s/bin\/ash/bin\/sh/" /etc/passwd

RUN npm install -g @angular/cli
RUN mkdir -p /opt/text2lex/ui
WORKDIR /opt/text2lex/ui
ADD package.json /opt/text2lex/ui/
RUN npm cache clean --force
RUN npm install
ADD . /opt/text2lex/ui

# Build
FROM node:alpine as build-stage
RUN apk add --update \
  curl \
  vim \
  bash \
  && rm /var/cache/apk/*
RUN npm install -g @angular/cli
WORKDIR /opt/text2lex/ui
COPY package*.json ./
RUN npm install
COPY . .
RUN ng build --prod

# Production
FROM nginx:1.13.12-alpine as production-stage
RUN apk add --update \
  curl \
  vim \
  bash \
  && rm /var/cache/apk/*
COPY ./nginx/entrypoint.sh /entrypoint.sh
COPY ./nginx/text2lex.conf /etc/nginx/conf.d/text2lex.conf
COPY --from=build-stage /opt/text2lex/ui/dist/ui /usr/share/nginx/html
CMD ["nginx", "-g", "daemon off;"]