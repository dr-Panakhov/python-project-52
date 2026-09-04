install:
	uv sync

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --no-input

setup: install collectstatic migrate

start:
	uv run python manage.py runserver

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh
