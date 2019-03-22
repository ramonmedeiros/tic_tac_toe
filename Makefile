test:
	pytest tests -v 

format-files:
	yapf -i -r tests tic_tac_toe

default: format-files
