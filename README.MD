Generic Django web app.

default super user

username: "admin"

password: "admin123"

# stack

1. django

2. postgres

3. redis

# requirements

- docker

- docker-compose

# getting started

1. build

```sh
docker compose up --build
```

2. create super user (optional)

```sh

docker compose exec backend bash

python manage.py createsuperuser

```

3. create user

- go to [ http://127.0.0.1:3035/admin ](http://127.0.0.1:3035/admin)

- go to "Users" in "AUTHENTICATION AND AUTHORIZATION" menu

- create new user and password

- go to "Nasabahs" in "DANA"

- create new nasabah
