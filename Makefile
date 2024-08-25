docker_django_createsuperuser:
	docker compose -f docker/docker-compose.yml run --rm django python manage.py createsuperuser

docker_django_makemigrations:
	docker compose -f docker/docker-compose.yml run --rm django python manage.py makemigrations

docker_django_migrate:
	docker compose -f docker/docker-compose.yml run --rm django python manage.py migrate

docker_django_pytest:
	docker compose -f docker/docker-compose.yml run --rm django pytest ${PYTEST_ARGS}

docker_django_coverage_report:
	docker compose -f docker/docker-compose.yml run --rm django sh -c "coverage run -m pytest && coverage report"

docker_build:
	docker compose -f docker/docker-compose.yml up -d --build

docker_stop:
	docker compose -f docker/docker-compose.yml stop

docker_rebuild:
	docker compose -f docker/docker-compose.yml stop && docker compose -f docker/docker-compose.yml up -d --build --remove-orphans

coverage_report:
	coverage run -m pytest
	coverage report

help:
	@echo "Usage: make [target]"
	@echo "Targets:"
	@echo "  docker_django_createsuperuser: create superuser"
	@echo "  docker_django_makemigrations: create migrations"
	@echo "  docker_django_migrate: apply migrations"
	@echo "  docker_django_pytest: run pytest with or without argument (eg. PYTEST_ARGS='-k test_1 -s')"
	@echo "  docker_django_coverage_report: generate coverage report"
	@echo "  docker_build: build docker images"
	@echo "  docker_stop: stop docker containers"
	@echo "  docker_rebuild: rebuild docker images"
	@echo "  coverage_report: generate coverage report"
