# API

## Notes

- All api methods prefixed with `/api` for flexibility and support for future
  expansion.
- Everything must be JSON, both in request and response bodies. The only
  exception may be when the server throws an error (oops).

### JWT required endpoints

Some API calls require a JSON web token (JWT) for authentication. If one below
is labelled "JWT required", then it requires authentication via a JWT (the one
you obtained by posting to `/api/token`).  This should be provided in the
`Authorization` header like so:

```
Authorization: `Bearer base64.encoded.jwt`,
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

See <https://jwt.io/> for more information on JWTs.

If an invalid JWT is supplied, the server will return a 401 response code.

### Common responses

All error responses will return a JSON object with a `"msg"` key giving more
information. For example:

```
{
  "msg": "username too long"
}
```

Additionally, for endpoints where a 200 success doesn't specify sending anything
back, as for example the `/api/play` endpoint, it will at least return a JSON
object with a `"msg"` as above. This can probably be safely ignored though.


## Endpoints

Summary:

- `/api/token` POST
- `/api/register` POST
- `/api/user` GET
- `/api/user/<username>` GET
- `/api/games` GET, POST
- `/api/games/<id>` GET, DELETE
- `/api/play` POST


### POST `/api/token`

Use your username and password to get a JWT to use for other API requests.


Example request body:

```
{
  "username": "user",
  "password": "qjknecawy"
}
```

Example response:

```
{
  "token": "base64.encoded.jwt"
}
```

### POST `/api/register`

Register a new user.

Example request body:

```
{
  "username": "neo",
  "password": "qjknecawy"
}
```

Example responses:

- 200 success

```
{
  "msg": "success"
}
```

- 400 invalid data submitted, not registered


### GET `/api/user`

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


### GET `/api/user/<username>`

Get JSON user details for `username`.  JWT required.

Example responses:

- 200 success:

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

- 404 user not found


### GET `/api/games`

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
      "can_delete": true,
      "language": "rop",
      "author": "username1"
    },
    {
      "id": 2,
      "word": "binana",
      "public": true,
      "can_delete": false,
      "language": "rop",
      "author": "username2"
    }
  ]
}
```

### POST `/api/games`

Create a new game, with JSON data supplied in the request body. JWT required.

Example request body:

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
- 400 data invalid in some way (see response for msg)


### GET `/api/games/<id>`

Get a single game's data in JSON. JWT required.

Example responses:

- 200 success:

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
  "pieces": ["na", "na", "bi"],
  "can_delete": false,
  "flags": [
    {
      "text": "spam flag :P",
      "user": "user123",
      "date": 150000000
    }
  ]
}
```

- 404 game not found


### DELETE `/api/games/<id>`

Delete a game. JWT required.

You can only delete a game if either you created the game, or you are an admin
and the game is public.

Example responses:

- 200 success:
- 401 not allowed to delete this game
- 404 game not found


### POST `/api/play`

Log a play/solve of a game. Data supplied in request body. JWT required.

Example request body:

```
{
  "id": "5"
}
```

Exammple responses:

- 200 successfully logged
- 404 game not found
- 400 invalid data in request body
