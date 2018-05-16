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

response:

200 success

```
{
  "msg": "success"
}
```

400 fail

### Authenticated methods below

The next methods require authentication via a JWT (the one you obtained by
posting to `/token`).
This should be provided in the `Authorization` header like so:

```
Authorization: `Bearer mybase64.encoded.token`,
```

Example of implementing this with [axios](https://github.com/axios/axios):

```
// your JWT
const token = 'some string';

// configure an instance with the header
const getAxiosAuthedInst = () => axios.create({
  baseURL: API_ROOT,
  headers: {
    Authorization: `Bearer ${token}`,
  },
});

// perform an api call
getAxiosAuthedInst().get('/user')...
```

See <https://jwt.io/> for more information on JSON Web Tokens.


### GET `/user`

Get your user details as json.  JWT required.

Example response:

```
{
  "username": "john",
  "is_admin": false,
  "n_plays": 5,
  "games_created": 1,
  "learner_score": 25,
  "creator_score": 10,
}
```


### GET `/usr/<username>`

Get JSON user details for `username`.  JWT required.

Example response:

```
{
  "username": "john",
  "is_admin": false,
  "n_plays": 5,
  "games_created": 1,
  "learner_score": 25,
  "creator_score": 10,
}
```


### GET `/games`

Get a JSON array of all games available to you (minimal information on each game
for bandwidth saving).  JWT required.

Future work may require adding pagination to this for scalability.

Example response:

```
{
  "games": [
    {
      "id": 1,
      "word": "epul",
      "public": true,
      "language": "rop"
    },
    {
      "id": 2,
      "word": "binana",
      "public": true,
      "language": "rop"
    }
  ]
}
```

### POST `/games`

Create a new game, with JSON data supplied in the request body. JWT required.

example request body:

```
{
  "images": [{
    "data": "base64 encoded blob"
  }],
  "audio": {
    "data": "base64 encoded blob"
  },
  "word": "epul",
  "public": true,
  "language": "rop"
}
```

responses:

- 200 success
- 400 invalid data posted


### GET `/games/<id>`

Get a single game's data in JSON. JWT required.

Example 200 response:

```
{
  "id": 4,
  "author": "myusername",
  "public": true,
  "word": "binana",
  "language": "rop",
  "images": [
      {
          "id": 0,
          "data": "base64 data url",
      }
  ],
  "pieces": ["na", "na", "bi"]
}
```


404 if not found




### POST `/play`

Log a play/solve of a game. Data supplied in request body. JWT required.

Example request body:

```
{
  "id": "5"
}
```

responses:

- 200 successfully logged
- 404 game not found
- 400 invalid data in request body
