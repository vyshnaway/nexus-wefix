.PHONY: help build up down logs migrate makemigrations superuser shell bash test demo

# Default target when just running 'make'
help:
	@echo "Nexus WeFix Commands:"
	@echo "-----------------------"
	@echo "make build          - Build or rebuild Docker containers"
	@echo "make up             - Start containers in the background"
	@echo "make down           - Stop and remove containers"
	@echo "make logs           - View output from containers"
	@echo "make migrate        - Run Django database migrations"
	@echo "make makemigrations - Generate new database migrations"
	@echo "make superuser      - Create a Django superuser interactively"
	@echo "make demo           - Generate demo data (admin, customers, workers, services)"
	@echo "make shell          - Open a Django Python shell"
	@echo "make bash           - Open a bash session inside the web container"
	@echo "make test           - Run Django test suite"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

migrate:
	docker-compose exec web python manage.py migrate

makemigrations:
	docker-compose exec web python manage.py makemigrations

superuser:
	docker-compose exec web python manage.py createsuperuser

demo:
	docker-compose exec web python manage.py create_demo_data

shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web bash

test:
	docker-compose exec web python manage.py test
