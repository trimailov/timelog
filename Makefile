env/bin/pip: env/bin/python requirements.txt
	env/bin/pip install -r requirements.txt

env/bin/python:
	virtualenv env

clean:
	rm -rf env

.PHONY: clean