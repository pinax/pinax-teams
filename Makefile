all: init test

init:
	python setup.py develop

test:
	coverage erase
	tox
	coverage html
