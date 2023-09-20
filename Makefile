PYTHON=python3

.PHONY: build-recreate
build-recreate:
	@docker-compose -f docker-compose.yml up --build --force-recreate

.PHONY: build
build:
	@docker-compose -f docker-compose.yml up --build

.PHONY: up
up:
	@docker-compose -f docker-compose.yml up

.PHONY: down
down:
	@docker-compose -f docker-compose.yml down

.PHONY: test
test:
	@docker exec -it fastapi-fido2 pytest -v

.PHONY: db-migrate
db-migrate:
	@docker exec -it fastapi-fido2 alembic -c alembic.ini revision --autogenerate -m "$(m)"

.PHONY: db-upgrade
db-upgrade:
	@docker exec -it fastapi-fido2 alembic -c alembic.ini  upgrade head

.PHONY: db-downgrade
db-downgrade:
	@docker exec -it fastapi-fido2 alembic -c alembic.ini  downgrade -1
