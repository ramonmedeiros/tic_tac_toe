TAG=tic_tac:local-container

test:
	pytest tests -v 

format-files:
	yapf -i -r tests tic_tac_toe

run:
	PYTHONPATH=. FLASK_APP=tic_tac_toe/app.py FLASK_ENV=development flask run

container:
	docker stop backend || true
	docker build . -t $(TAG)
	docker run --name backend --rm -d $(TAG)

default: format-files


