
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


## Resource files

The [PMI](https://en.wikipedia.org/wiki/Pointwise_mutual_information) based word
segmentation algorithm requires training on a list of sample words in a
language to work correctly. The MVP supports Kriol only, and attempts to load a
list of kriol words from `res/kriol.txt`, where the list is formatted as
plaintext with one word per line. Example file:

```
thred
thri
thribala
thribalawei
thridei
```

The production server loads from a file containing a list of 5000 kriol words,
which is not distributed with the source code due to copyright concerns.

Before running the server, please create a `kriol.txt` file in the `res`
directory. The server should work even if it is empty, but for better word
segmentation, as many Kriol words as possible should be entered into the file.


## Development


```
git clone git@github.com:swalladge/dhoyu-server.git
cd dhoyu-server

# create the pmi resource file with at least one word
# see above section for recommendations
mkdir res
echo 'word' > res/kriol.txt

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

See docs at [docs/API.md](docs/API.md).


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
