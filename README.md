# clacket
Movie recommendation engine and other things we're thinking through.
WE HAVE A NAME.

## Members
- Mariam, [@blaringsilence](https://github.com/mariamrf).
- Tarek, [@TarekSamirJedi](https://github.com/TarekSamirJedi).

## Install/Run
1. Clone the github repo
2. Install virtualenv and activate it

	```bash
		$ virtualenv -p python3 venv
		$ . venv/bin/activate
	```
3. Install requirements

	```bash
		$ make bootstrap
	```

## Save changes to installed packages before commiting (so environment is the same with everyone)
1. Freeze requirements

	```bash
		$ pip freeze -l > requirements.txt
	```
2. Commit changes as you would normally with git
3. To deactivate the virtualenv, simply:

	```bash
		$ deactivate
	```

## Test and Lint Python
(Testing lints but linting doesn't test)
```bash
		$ make lint
		$ make test
```
