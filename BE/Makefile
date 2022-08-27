postgres-test:
	docker run -d --name test_db -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test_db -p 5432:5432  postgres
createdb:
	docker exec -it postgres14 createdb --username=postgres --owner=root hybe
dropdb:
	docker exec -it postgres14 dropdb postgres
test:
	coverage run -m pytest
server:
	uvicorn app.main:app --port 8000 --reload
report:
	coverage report -m
rebuildBE:
	docker-compose up --build backend
rebuildDB:
	docker-compose up --build database
lint:
	flake8
.PHONY: postgres-test createdb dropdb test server rebuildBE rebuildDB lint