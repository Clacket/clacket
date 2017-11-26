test:
	make clean
	make lint
	@py.test --disable-pytest-warnings tests/
	make clean

lint:
	@flake8 . --exclude venv,docs
	# @pylint . --rcfile=pylintrc

clean:
	@find . -type f -name '*.pyc' -delete
	@find . -type d -name '__pycache__' -delete

clear-saved:
	@rm -rf /media/mariam/Files/ran/clacket-save/*

count-saved:
	@ls /media/mariam/Files/ran/clacket-save | wc -l

bootstrap:
	# @pip install -r dev_requirements.txt
	@pip install -r requirements.txt
	@pip install -e .
	@flake8 --install-hook git || true
	@git config --bool flake8.strict true || true