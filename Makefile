test:
	pytest tests -v 

format-files:
	yapf -i -r tests tic_tac_toe

run:
	FLASK_APP=tic_tac_toe/app.py FLASK_ENV=development flask run

default: format-files


