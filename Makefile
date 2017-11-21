test:
	make clean
	make lint
	@py.test --disable-pytest-warnings tests/

lint:
	@flake8 . --exclude venv,docs
	# @pylint . --rcfile=pylintrc

clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete

bootstrap:
	# @pip install -r dev_requirements.txt
	@pip install -r requirements.txt
	@pip install -e .
	@flake8 --install-hook git || true
	@git config --bool flake8.strict true || true