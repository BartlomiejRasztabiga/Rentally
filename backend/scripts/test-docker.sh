#! /usr/bin/env bash

docker-compose down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error

docker-compose build
docker-compose up -d
docker-compose exec -T backend bash ./prestart.sh
docker-compose exec -T backend bash ./tests-start.sh
docker-compose down -v --remove-orphans
