postgres:
	docker run --name hybe -p 5432:5432 -e POSTGRES_PASSWORD=example -d postgres
createdb:
	docker exec -it postgres14 createdb --username=postgres --owner=root hybe
dropdb:
	docker exec -it postgres14 dropdb hybe
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
.PHONY: postgres createdb dropdb test server rebuildBE rebuildDB