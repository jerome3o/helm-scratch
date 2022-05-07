FROM python:3.8

RUN pip install pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy

COPY index.py .

CMD ["pipenv", "run", "prod"]
