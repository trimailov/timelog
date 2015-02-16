env/bin/pip: env/bin/python requirements.txt
	env/bin/pip install -r requirements.txt

env/bin/python:
	virtualenv env

test:
	env/bin/python tests.py

clean:
	rm -rf env tags

tags:
	ctags -R

freeze:
	env/bin/pip freeze > requirements.txt

.PHONY: test clean_test clean tags freeze
