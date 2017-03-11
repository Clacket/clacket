# clacket
Movie recommendation engine and other things we're thinking through.
WE HAVE A NAME.

## Members
- Mariam, [@blaringsilence](https://github.com/blaringsilence).
- Tarek, [@TarekSamirJedi](https://github.com/TarekSamirJedi).

## Install/Run
1. Clone the github repo

	```bash
		$ git clone https://github.com/blaringsilence/clacket.git
		$ cd clacket
	```
2. Install virtualenv and activate it

	```bash
		$ pip install virtualenv
		$ virtualenv -p python3 venv
		$ . venv/bin/activate
	```
3. Install requirements

	```bash
		$ pip install -r requirements.txt
	```

## Save changes to installed packages before commiting (so environment is the same with everyone)
1. Freeze requirements

	```bash
		$ pip freeze > requirements.txt
	```
2. Commit changes as you would normally with git
3. To deactivate the virtualenv, simply:

	```bash
		$ deactivate
	```
