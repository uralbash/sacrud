all: test

test:
	nosetests --with-coverage --cover-package sacrud --cover-erase --with-doctest --nocapture

coverage: test
	coverage html

run:
	pserve development.ini

shell:
	pshell development.ini
