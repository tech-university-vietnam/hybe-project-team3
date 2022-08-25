postgres:
	docker run --name hybe -p 5432:5432 -e POSTGRES_PASSWORD=example -d postgres
createdb:
	docker exec -it postgres14 createdb --username=postgres --owner=root hybe
dropdb:
	docker exec -it postgres14 dropdb hybe
test:
	coverage run -m pytest
server:
	uvincorn app.main:app --port 8000
report:
	coverage report -m
.PHONY: postgres createdb dropdb test server