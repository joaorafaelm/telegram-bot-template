.PHONY: all help test clean migrations migrate run deploy

MANAGER=pipenv run python manage.py

all: 
	@echo "try 'make help'"

help: # show all commands
	@sed -n 's/:.#/:/p' makefile | grep -v @

test: # run tests
	pipenv run pytest

clean: # clean cached files
	@find . -name \*.pyc -o -name \*.pyo -o -name __pycache__ -exec rm -rf {} +
	@echo 'all __pycache__, *.pyc, *.pyo files were removed'

migrations: # create migrations
	$(MANAGER) makemigrations --no-header

migrate: # apply migrations
	$(MANAGER) migrate

run: # run bot
	pipenv run python -m bot
