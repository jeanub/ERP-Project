Dev:
cp .env.dev .env
make dev
make init-frontend
Abrí http://localhost:5173 y http://localhost:8000/api/ping

Prod:
cp .env.prod .env
make build-prod
make up-prod
