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
	docker run -p 5000:5000 --name backend --rm -d $(TAG)


run-fronted:
	PYTHONPATH=. FLASK_APP=frontend/server.py FLASK_ENV=development flask run  --port=8080

default: format-files

setup:
	virtualenv --python=python3.6 .venv
	source .venv/bin/activate && pip install -r requirements.txt


