.PHONY: install migrate run front server

install:
	@pip install -r requirements.txt
	@npm install

admin:
	@python manage.py createsuperuser

migrate:
	@python manage.py migrate

front:
	@npm start

server:
	@prefect backend server
	@python manage.py runserver 0.0.0.0:8000

run: | front server
