# SW API GraphQL

## Requirements

* [Python](https://www.python.org/) (realizado en python 3.8)
* [Django](https://github.com/django/django)
* [Django Filter](https://github.com/carltongibson/django-filter)
* [Django model utils](https://github.com/jazzband/django-model-utils)
* [Graphene](https://github.com/graphql-python/graphene-django)
* [.EVN](https://github.com/theskumar/python-dotenv)

## Setup

Clone the project

```
git clone https://github.com/gustav0/swapi.git
```

Move into de repo and install dependencies

```
pip install -r requirements.txt
```

Create a .env file with a secret key or [get one](https://djecrety.ir/) manually and set it in the settings.py

```
python -c "from django.core.management.utils import get_random_secret_key;  print(f'SECRET_KEY = {get_random_secret_key()}')" > swapi/.env 
```

Run migrations and load fixtures

```
python manage.py migrate
python manage.py load_fixtures
```

Now the project is all set.

### Running the server

```
python manage.py runserver
```

### Runing the tests

```
python manage.py test
```

## Extras

Agregué un collection de postman dentro del directorio `extra` del repositorio, el cual contiene todos los request ya armados para hacer pruebas (le quité todas las variables del environment para que no tengan que crear nada, si se me pasó alguna me disculpo).

## Notas
