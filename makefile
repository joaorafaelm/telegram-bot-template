.PHONY: all help test clean migrations migrate run deploy
.ONESHELL:

-include .env
export

VENV=.venv/bin/
MANAGER=$(VENV)python manage.py

all: help

help: # show all commands
	@sed -n 's/:.#/:/p' makefile | grep -v @

venv: # create virtual environment
	@python3 -m venv .venv
	@$(VENV)pip install -U pip -q

install: venv # install dependencies
	@$(VENV)pip install -r requirements.txt -q

lock: venv # update dependencies
	@sed -i '' 's/[~=]=/>=/' requirements.txt
	@$(VENV)pip install -U -r requirements.txt
	@$(VENV)pip freeze -r requirements.txt | awk '/.*pip freeze.*/ {exit} {print}' > requirements-lock.txt
	@sed -i '' 's/==/~=/' requirements-lock.txt
	@sort -o requirements-lock.txt requirements-lock.txt
	@mv requirements-lock.txt requirements.txt

test: # run tests
	@$(VENV)pytest

clean: # clean cached files
	@find . -name \*.pyc -o -name \*.pyo -o -name __pycache__ -exec rm -rf {} +
	@echo 'all __pycache__, *.pyc, *.pyo files were removed'

migrations: # create migrations
	$(MANAGER) makemigrations --no-header

migrate: # apply migrations
	$(MANAGER) migrate

run: # run bot
	@$(VENV)honcho start
