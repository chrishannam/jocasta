test:
	PYTHONPATH=. pytest --cov jocasta --cov-report term-missing -s -p no:warnings --log-cli-level error
