COMPOSE = docker compose
ENV_FILE ?= .env.dev

up:
	$(COMPOSE) --env-file $(ENV_FILE) --profile dev up -d --build

down:
	$(COMPOSE) --env-file $(ENV_FILE) down -v

logs:
	$(COMPOSE) --env-file $(ENV_FILE) logs -f --tail=200

sh-backend:
	$(COMPOSE) --env-file $(ENV_FILE) exec backend sh

sh-frontend:
	$(COMPOSE) --env-file $(ENV_FILE) exec frontend sh

migrate:
	$(COMPOSE) --env-file $(ENV_FILE) exec backend python manage.py migrate

createsuperuser:
	$(COMPOSE) --env-file $(ENV_FILE) exec -it backend python manage.py createsuperuser

collectstatic:
	$(COMPOSE) --env-file $(ENV_FILE) exec backend python manage.py collectstatic --noinput

init-frontend:
	$(COMPOSE) --env-file $(ENV_FILE) run --rm frontend sh -lc "npm create vite@latest . -- --template react && npm i && npm i -D tailwindcss postcss autoprefixer && npx tailwindcss init -p"

dev: up

build-prod:
	$(COMPOSE) --env-file .env.prod --profile prod run --rm frontend_build

up-prod:
	$(COMPOSE) --env-file .env.prod --profile prod up -d --build nginx backend_prod celery beat db redis

down-prod:
	$(COMPOSE) --env-file .env.prod --profile prod down -v
