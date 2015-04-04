env/bin/pip: env/bin/python requirements.txt
	env/bin/pip install -r requirements.txt

env/bin/python:
	virtualenv env

test:
	env/bin/python tests.py

coverage:
	rm -rf htmlcov/ .coverage
	env/bin/coverage run --omit='env/*' tests.py
	coverage report -m
	coverage html
	@echo "Now you can use:"
	@echo "open htmlcov/index.html"

show_coverage:
	open htmlcov/index.html

clean:
	rm -rf env tags htmlcov .coverage timeflow.egg-info

tags:
	ctags -R

freeze:
	env/bin/pip freeze > requirements.txt

.PHONY: test clean_test clean tags freeze
