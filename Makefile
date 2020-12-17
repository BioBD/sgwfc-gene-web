.PHONY: install migrate run front server

install:
	@pip install -r requirements.txt
	@npm install

migrate:
	@python manage.py migrate

front:
	@npm start

server:
	@prefect backend server
	@python manage.py runserver

run: | front server