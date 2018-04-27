
# Dhoyu api server

Copyright © 2018 Samuel Walladge


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

