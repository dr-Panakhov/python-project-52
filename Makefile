install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py tailwind build
	uv run python manage.py collectstatic --no-input

setup: install collectstatic migrate

start:
	uv run python manage.py runserver

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

git:
	git add .
	git commit -m "auto fix"
	git push

test:
	uv run pytest

test-coverage:
	uv run pytest --cov=task_manager --cov-report=xml users/
