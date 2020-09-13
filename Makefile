deploy: test clean install build push

test:
	PYTHONPATH=. pytest --cov jocasta --cov-report term-missing -s -p no:warnings --log-cli-level error

clean:
	@echo "Cleaning up..."
	rm -rf dist build sdist bdist_wheel jocasta.egg-info

install:
	python setup.py install

build:
	python setup.py sdist bdist_wheel

push:
	python -m twine upload dist/*
