FROM python:3.6

WORKDIR /app

COPY . /app/

RUN pip install -r /app/requirements.txt

EXPOSE 5000
ENV PYTHONPATH=.
ENV FLASK_APP=tic_tac_toe/app.py
CMD ["flask", "run", "--host=0.0.0.0"]
