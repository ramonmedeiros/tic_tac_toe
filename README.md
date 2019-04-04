# Ramon's tic tac toe

## How to run

* Unzip the folder
* run ```make setup```. This will create a virtualenv and install dependencies
* You can run tests ```make test``` to make sure it's working 
* You'll need to run both backend and frontend. So: ```make run``` and ```make run-frontend```

## Backend architecture

The backend is basically a python class (game.py), which has the "business rules", or game rules. The REST API is on app.py. which uses flask framework to create the HTTP server.
In tests folder, I wrote unit and integration tests while developing it to make sure that new changes won't affect the functionality. 

Backend runs on localhost:5000

Frontend runs on http://localhost:8080

(Game should be played without RTFM)

## Frontend architecture

Frontend uses a base template and javascript to interact with backend. No frameworks were used, only functions available on Chrome.


## Game features
* To play, you need to login (just set the username)
* You can watch all games
* You can share game url

