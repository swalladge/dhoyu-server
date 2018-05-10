
# Dhoyu Server

Copyright © 2018 Samuel Walladge


## About

This is the server that the [Dhoyu](https://github.com/swalladge/dhoyu-mobile)
mobile app depends on.  It provides a JSON api endpoint that manages access to a
database storing user data and games.

### The Dhoyu project

This repository is part of a thesis on mobile games for Aboriginal languages.

Canonical sources are available at the following urls:

- dhoyu-mobile: <https://github.com/swalladge/dhoyu>
- dhoyu-server: <https://github.com/swalladge/dhoyu-server>


## Development

```
git clone git@github.com:swalladge/dhoyu-server.git
cd dhoyu-server
pipenv install
pipenv install --dev

# edit .env to add env vars (recommend those below:)
# export FLASK_APP=dhoyu
# export FLASK_ENV=development
vi .env

# init the database and insert demo data (see dhoyu/__init__.py for details)
pipenv run flask db-demo

# run the dev server!
pipenv run flask run

# run.sh for convenience - binds to all interfaces
./run.sh
```

Recommend putting a `config.py` in `instance/` for persistant local config.


## API

### POST `/token`

Use your username and password to get a JWT to use for other API requests.


send in body:

```
{
  "username": "user",
  "password": "qjknecawy"
}
```

response:

```
{
  "token": "base64.encoded.jwt"
}
```

### POST `/register`

Register a new user.

send in body:

```
{
  "username": "user",
  "password": "qjknecawy"
}
```

response code will tell you if it worked


### GET `/user`

get your user details as json


### GET `/usr/<username>`

get json user details for `username`


### GET `/games`

get a json array of games (minimal information on each game for bandwidth
saving)


### POST `/games`

create a new game

TODO: stabilize and describe body format to send


### GET `/games/<name>`

get a game's data in json



## Deploying

Clone and install dependencies:

```
git clone git@github.com:swalladge/dhoyu-server.git
cd dhoyu-server
pipenv install
```

Install `gunicorn`

```
pipenv run pip install gunicorn
```

Add a `.env` file with the following contents:

```
!/bin/bash

export FLASK_APP=dhoyu
export FLASK_ENV=production
```

Init the database:

```
pipenv run flask db-up

# or if you want demo data
pipenv run flask db-demo
```


Configure:

```
mkdir instance
vi instance/config.py
```

You'll want to at least add the `SECRET_KEY` config option there for security.
Example contents (remember it must be valid python):

```
SECRET_KEY='asdfasdfasdf'
SQLALCHEMY_ECHO=False
```

Run:

```
pipenv run gunicorn -w 4 -b 127.0.0.1:8000 dhoyu:app

# or with fancy logging
pipenv run gunicorn -w 4 -b 127.0.0.1:8000 \
  --log-file debug.log --log-level DEBUG \
  --access-logfile access.log \
  dhoyu:app
```

For convenience you will probably want that run line put into a service file or
something so that it will automatically start on reboot.

Finally, configure a reverse proxy such as nginx so it's accessible to the
outside world.



## License

    Dhoyu Server
    Copyright (C) 2018 Samuel Walladge

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
