.PHONY: dev up down logs test lint

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

up:
	docker compose up -d --build

down:
	docker compose down

logs:
	docker compose logs -f --tail=200

test:
	pytest -q

lint:
	ruff check .
