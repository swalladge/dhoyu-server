
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

`./run.sh`

or 

```
export FLASK_APP=dhoyu
export FLASK_ENV=development
pipenv run flask <command>
```

- put a `config.py` in `instance/` for persistant local config


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
