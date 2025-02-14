.DEFAULT_GOAL := help
.PHONY: help dev

## Build docker images
build:
	docker compose build

build-no-cache:
	docker compose build --no-cache

build-debug:
	docker compose -f docker-compose.debug.yml \
		build

build-prod:
	docker compose -f docker-compose.prod.yml \
		build


## Run all services
up:
	docker compose up --remove-orphans

up-debug:
	docker compose -f docker-compose.debug.yml \
		up --remove-orphans

up-prod:
	docker compose -f docker-compose.prod.yml \
		run web python manage.py collectstatic --no-input --clear
	docker compose -f docker-compose.prod.yml \
		up


## Bring down all services
down:
	docker compose down

down-debug:
	docker compose -f docker-compose.debug.yml \
		down

down-prod:
	docker compose -f docker-compose.prod.yml \
		down
	# Delete replica volumes matching regex pattern
	#docker volume ls | egrep -wo 'db_replica.[a-z_]*' | xargs -r docker volume rm


## Clean containers
clean:
	docker container prune -f

nuke:
	make down
	make clean
	#docker volume prune -af


## Run tests
test-backend: ## Run all Django tests
	docker compose run --rm web pytest


## Run linters and formatters
lint-check:
	docker compose run --rm web ruff check
	docker compose run --rm app yarn biome lint

lint-fix:
	docker compose run --rm web ruff --fix
	docker compose run --rm app yarn biome lint --write

format-check:
	docker compose run --rm web ruff format --check
	docker compose run --rm app yarn biome format

format-fix:
	docker compose run --rm web ruff format
	docker compose run --rm app yarn biome format --write


## Access running containers
sh: ## Open a shell with all dependencies
	docker compose run --rm web sh

sh-app: ## Open a shell with all dependencies
	docker compose run --rm app sh

django-sh:
	docker compose run --rm web python manage.py shell

psql: ## Open a Postgres shell
	docker compose run --rm web python manage.py dbshell


## Initialize data stores with starting data
createsuperuser: ## Create the root Django superuser with username=root password=root
	docker compose \
	    run \
	    -e DJANGO_SUPERUSER_PASSWORD=root \
	    -e DJANGO_SUPERUSER_USERNAME=root \
	    -e DJANGO_SUPERUSER_EMAIL=root@example.com \
	    web \
	    python manage.py createsuperuser --noinput

createusers: ## Create 2 standard users username=user1 and username=user2
	docker compose \
		run \
		web \
		python manage.py shell --command "from django.contrib.auth.models import User; User.objects.create_superuser(username='user1', email='user1@example.com', password='password')"
	docker compose \
		run \
		web \
		python manage.py shell --command "from django.contrib.auth.models import User; User.objects.create_superuser(username='user2', email='user2@example.com', password='password')"

createsuperuser-prod: ## Create the root Django superuser with username=root password=root
	docker compose -f docker-compose.prod.yml \
	    run \
	    -e DJANGO_SUPERUSER_PASSWORD=root \
	    -e DJANGO_SUPERUSER_USERNAME=root \
	    -e DJANGO_SUPERUSER_EMAIL=root@example.com \
	    web \
	    python manage.py createsuperuser --noinput

createusers-prod: ## Create 2 standard users username=user1 and username=user2
	docker compose -f docker-compose.prod.yml \
		run \
		web \
		python manage.py shell --command "from django.contrib.auth.models import User; User.objects.create_superuser(username='user1', email='user1@example.com', password='password')"
	docker compose -f docker-compose.prod.yml \
		run \
		web \
		python manage.py shell --command "from django.contrib.auth.models import User; User.objects.create_superuser(username='user2', email='user2@example.com', password='password')"

hydrate: ## Populate db with initial tickers and price data
	docker compose run web python manage.py hydrate

hydrate-prod:
	docker compose -f docker-compose.prod.yml \
		run web python manage.py hydrate

migrate: ## Create and apply database migrations
	docker compose run --rm web python manage.py makemigrations
	docker compose run --rm web python manage.py migrate
	docker compose run --rm web python manage.py migrate --database=celerybeat

migrate-prod:
	docker compose -f docker-compose.prod.yml \
		run --rm web python manage.py migrate
	docker compose -f docker-compose.prod.yml \
		run --rm web python manage.py migrate --database=celerybeat


init:
	make build
	make migrate
	make createsuperuser
	make createusers
	#make hydrate
	docker compose stop --remove-orphans

init-prod:
	make build-prod
	make migrate-prod
	make createsuperuser-prod
	make createusers-prod
	#make hydrate-prod
	docker compose stop --remove-orphans


open-admin: ## Open the Django admin page
	open http://localhost:8000/admin

open-app: ## Open the React app
	open http://localhost:3000

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
