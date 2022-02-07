# LQN - TEST

## Requirements

* [Python](https://www.python.org/) (Developed on Python 3.8)
* [Django](https://github.com/django/django)
* [Django Filter](https://github.com/carltongibson/django-filter)
* [Django model utils](https://github.com/jazzband/django-model-utils)
* [Graphene](https://github.com/graphql-python/graphene-django)
* [.EVN](https://github.com/theskumar/python-dotenv)

## TEST 1 - LOGIC

### Buzz-Bazz

In this problem I had to code an algorithm that cicles through 0-100 printing those numbers, it also has to print buzz on the same line in case the name is even, and bazz if it is multiple of 5.

The algorithm has O(n) time speed, because it goes through the elements once.

### Pokemon first letter - last letter

The task was a more complex than the first one, basically I had to find a way to get the longest route of consecutive names having the last letter of the preceding name.

I googled the longest path possible algorithm, and fin a way to solve it. The only problem I encountered was that I couldn't find a way to remove repeated elements and getting a node back (I visualized the problem as tree nodes).

I found help on StackOverflow and ended with a solution.

## Test 2 - Swapi

### Introduction

For this problem I had multiple chores, I had to add new fields in the Models, add new mutations and test.

GraphQL was completely new for me so I had to google everything to get the job done. Also I read the addPlanet mutation to understand a bit how to implement the auxiliary generic mutation.

### Installation

To get running the project you MUST follow this steps:

1. **Clone the project into a empty directory.**

   ```
   git clone https://github.com/Sarsu12/LQN-test.git
   ```
2. **Get into stars-wars directory and install dependencies.**

   ```
   pip install -r requirements.txt
   ```
3. **Create a .env file with a secret key to run the Django Project. Use the following command:**

   ```
   python -c "from django.core.management.utils import get_random_secret_key;  print(f'SECRET_KEY = {get_random_secret_key()}')" > swapi/swapi/.env 
   ```

   ***Note: Make sure you are on the stars-wars directory before running this command.***
4. **Run the migrations to initialize the database and load the fixtures to add data into it.**

   ```
   python manage.py migrate
   python manage.py load_fixtures
   ```
5. **Done, now you may run the server.**

### Running the server

    `` python manage.py runserver ``

### Queries / Mutations

To make any query or mutation you must get into

```
http://127.0.0.1:8000/graphql
```

The GraphiQL interface is enabled on ***urls.py***, so you can make any operation on that endpoint.

### Runing the tests

To run the test file you need to type:

```
python manage.py test app.test
```

## Extras

* I did all the TODOs I found.
* Tried doing Flake8 formatting into all code I added.

## Notes

* Due to the few amount of documentation on graphene and graphene_django I might need to read and learn more on the go.
* The graphene_django library use on this exercise is a bit deprecated, using Django 2.1 limits the capability of using ChoiceFields and transforming them into enums with graphene.
* I couldn't find a way to test the mutations and queries using Pytest.
