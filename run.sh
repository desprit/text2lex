#!/bin/bash

# Terminal colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

# Project settings
DIR=`dirname $0`
PROJECT_NAME='text2lex'

ALL_CONTAINERS=(
  "$PROJECT_NAME"_redis
  "$PROJECT_NAME"_postgres
  "$PROJECT_NAME"_frontend
  "$PROJECT_NAME"_api
  "$PROJECT_NAME"_nlp
  end
)
DEV_CONTAINERS=(
  "$PROJECT_NAME"_redis
  "$PROJECT_NAME"_postgres
  "$PROJECT_NAME"_frontend
  "$PROJECT_NAME"_api
  "$PROJECT_NAME"_nlp
  end
)
PROD_CONTAINERS=(
  "$PROJECT_NAME"_redis
  "$PROJECT_NAME"_postgres
  "$PROJECT_NAME"_frontend
  "$PROJECT_NAME"_api
  "$PROJECT_NAME"_nlp
  end
)

# COMMON FUNCTIONS

clean() {
  # Clean system from dungling docker images and stopped containers
  yes | docker system prune
  printf "${GREEN}Cleaned.${NC}\n"
}

truncate() {
  # Reset all log files for the project
  sudo find /var/log/$PROJECT_NAME -type f -name "*.log" -exec truncate -s 0 {} +
  printf "${GREEN}All log files are reset.${NC}\n"
}

log() {
  tail -F \
    /var/log/$PROJECT_NAME/api/err.log \
    /var/log/$PROJECT_NAME/api/out.log \
    /var/log/$PROJECT_NAME/api/supervisord.log \
    /var/log/$PROJECT_NAME/nlp/err.log \
    /var/log/$PROJECT_NAME/nlp/out.log \
    /var/log/$PROJECT_NAME/nlp/supervisord.log \
    /var/log/$PROJECT_NAME/frontend/nginx_err.log \
    /var/log/$PROJECT_NAME/frontend/nginx_out.log
}

stop() {
  env=${1:-"dev"}
  if [[ $env == "prod" ]] ; then
    docker-compose -f $DIR/configs/docker-compose.yml -f $DIR/configs/docker-compose.prod.yml stop 2>/dev/null
  else
    docker-compose -f $DIR/configs/docker-compose.yml -f $DIR/configs/docker-compose.dev.yml stop 2>/dev/null
  fi
  printf "${GREEN}Containers are stopped.${NC}\n"
  status
}

status() {
  running=$(docker ps)
  for i in ${ALL_CONTAINERS[@]}; do
    if [[ $running == *"$i"* ]] && [ $i != 'end' ] ; then
      printf "${GREEN}$i is running.${NC}\n"
    elif [[ $running != *"$i"* ]] && [ $i != 'end' ] ; then
      printf "${RED}$i isn't running.${NC}\n"
    fi
  done
}

prepare() {
  if [ ! -f .env ]; then
    echo -e "# This file is just to make IDE know about project structure\nPYTHONPATH=$PWD:$PWD/backend/api/src:$PWD/backend/nlp/src:$PWD/venv/lib/python3.7/site-packages" >> .env
  fi
  sudo mkdir -p /data/text2lex
  sudo mkdir -p /var/log/$PROJECT_NAME/api
  sudo mkdir -p /var/log/$PROJECT_NAME/nlp
  sudo mkdir -p /var/log/$PROJECT_NAME/frontend
  sudo touch /var/log/$PROJECT_NAME/api/out.log
  sudo touch /var/log/$PROJECT_NAME/api/err.log
  sudo touch /var/log/$PROJECT_NAME/api/supervisord.log
  sudo touch /var/log/$PROJECT_NAME/nlp/out.log
  sudo touch /var/log/$PROJECT_NAME/nlp/err.log
  sudo touch /var/log/$PROJECT_NAME/nlp/supervisord.log
  sudo touch /var/log/$PROJECT_NAME/frontend/nginx_out.log
  sudo touch /var/log/$PROJECT_NAME/frontend/nginx_err.log
  sudo chown -R root:$USER /var/log/$PROJECT_NAME
  sudo chown -R root:$USER /data/text2lex
  sudo chmod 2775 /var/log/$PROJECT_NAME
  sudo chmod 2775 /data/text2lex
  find /var/log/$PROJECT_NAME -type d -exec sudo chmod 2775 {} +
  find /data/text2lex -type d -exec sudo chmod 2775 {} +
  find /var/log/$PROJECT_NAME -type f -exec sudo chmod 0664 {} +
  find /data/text2lex -type f -exec sudo chmod 0664 {} +
}

dev() {
  docker-compose -f $DIR/configs/docker-compose.yml -f $DIR/configs/docker-compose.dev.yml up -d --build
  sleep 5
  running=$(docker ps)
  # Check that required containers are running
  for i in ${DEV_CONTAINERS[@]}; do
    if [[ $running != *"$i"* ]] && [ $i != 'end' ] ; then
      printf "${RED}$i isn't running.${NC}\n"
      stop
      break
    fi
    # When all containers are checked, report status and start logs tailing
    if [ $i == 'end' ]; then
      status
      docker-compose -f $DIR/configs/docker-compose.yml -f $DIR/configs/docker-compose.dev.yml logs -f
    fi
  done
}

prod() {
  docker-compose -f $DIR/configs/docker-compose.yml -f $DIR/configs/docker-compose.prod.yml up -d --build
  sleep 5
  running=$(docker ps)
  # Check that required containers are running
  for i in ${PROD_CONTAINERS[@]}; do
    if [[ $running != *"$i"* ]] && [ $i != 'end' ] ; then
      printf "${RED}$i isn't running.${NC}\n"
      stop
      break
    fi
  done
}

recreateDb() {
  docker exec -it outbookers_api python -m shared.database.db_utils -t drop_db
  docker exec -it outbookers_api python -m shared.database.db_utils -t init_db
  docker exec -it outbookers_api python -m shared.database.db_utils -t drop_db --name outbookers_test
  docker exec -it outbookers_api python -m shared.database.db_utils -t init_db --name outbookers_test
}

test() {
  coverage erase
  PYTHONPATH=/home/desprit/projects/text2lex:/home/desprit/projects/text2lex/backend/api/src:/home/desprit/projects/text2lex/backend/nlp/src:/home/desprit/projects/text2lex/venv/lib/python3.7/site-packages coverage run -m unittest shared/tests/runner.py
  coverage html --rcfile .coveragerc -d htmlcov
}

run_redis() {
  name=$(docker ps --filter "name="$PROJECT_NAME"_redis" --format "{{.ID}}")
  if [[ -z "$name" ]] ; then
    printf "${YELLOW}Container "$PROJECT_NAME"_redis not found.${NC}\n"
    exit
  fi
  # Find Redis password based on provided environment
  if [[ $1 == "cli" ]] ; then
    if [[ $2 == "prod" ]] ; then
      REDIS_PASS=$(grep REDIS_PASS configs/.prod.env | xargs)
    else
      REDIS_PASS=$(grep REDIS_PASS configs/.dev.env | xargs)
    fi
    REDIS_PASS=${REDIS_PASS#*=}
    docker exec -it $name redis-cli -a $REDIS_PASS
  else
    docker exec -it $name /bin/sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec sh"
  fi
}
run_api() {
  docker exec -it "$PROJECT_NAME"_api /bin/bash
}
run_nlp() {
  docker exec -it "$PROJECT_NAME"_nlp /bin/bash
}
run_frontend() {
  docker exec -it "$PROJECT_NAME"_frontend /bin/sh -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec sh"
}
run_psql() {
  name=$(docker ps --filter "name="$PROJECT_NAME"_postgres" --format "{{.ID}}")
  docker exec -it $name /bin/bash -c "export COLUMNS=`tput cols`; export LINES=`tput lines`; exec bash"
}


show_usage() {
  echo ""
  printf "${YELLOW}Supported arguments:${NC}\n\n"
  printf "  ${GREEN}-h/help${NC} - show available commands;\n"
  printf "  ${GREEN}truncate${NC} - truncate to 0 all project log files;\n"
  printf "  ${GREEN}log${NC} - tail log files of aiohttp, nginx;\n"
  printf "  ${GREEN}prepare${NC} - create folders required for the project;\n"
  printf "  ${GREEN}test${NC} - run unit tests;\n"
  printf "  ${GREEN}recreatedb${NC} - recreate test and main databases;\n"
  printf "  ${GREEN}stop${NC} - stop all containers;\n"
  printf "  ${GREEN}dev${NC} - run development services;\n"
  printf "  ${GREEN}status${NC} - show state of all containers;\n"
  printf "  ${GREEN}redis cli${NC} - connect to Redis container;\n"
  printf "  ${GREEN}postgres${NC} - connect to Postgres container;\n"
  printf "  ${GREEN}api${NC} - connect to API container;\n"
  printf "  ${GREEN}nlp${NC} - connect to NLP container;\n"
  printf "  ${GREEN}frontend${NC} - connect to VueJS container;\n"
  echo ""
}

COMMAND=${1:-"dev"}

if   [ $COMMAND = "-h" ]         ; then show_usage
elif [ $COMMAND = "help" ]       ; then show_usage
elif [ $COMMAND = "trunc" ]      ; then truncate
elif [ $COMMAND = "log" ]        ; then log
elif [ $COMMAND = "prepare" ]    ; then prepare
elif [ $COMMAND = "test" ]       ; then test
elif [ $COMMAND = "recreatedb" ] ; then recreateDb
elif [ $COMMAND = "stop" ]       ; then stop $2
elif [ $COMMAND = "dev" ]        ; then prepare && stop && dev $2
elif [ $COMMAND = "prod" ]       ; then prepare && stop && prod
elif [ $COMMAND = "status" ]     ; then status
elif [ $COMMAND = "redis" ]      ; then run_redis $2 $3
elif [ $COMMAND = "postgres" ]   ; then run_psql
elif [ $COMMAND = "api" ]        ; then run_api
elif [ $COMMAND = "nlp" ]        ; then run_nlp
elif [ $COMMAND = "frontend" ]   ; then run_frontend
fi