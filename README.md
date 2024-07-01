# HTTP server

**Basic server for basic needs.**

## Headers  # commit 9

- `Content-Type`
- `Content-Length`
- `Accept`
- `User-Agent`
- `Host`
- `Accept-Encoding`

## Types of requests

- GET / - returns a 200 OK
- GET /echo/{string} - returns the string
- GET /user-agent - returns the user agent
- GET /files/{path} - returns the file's content  # commit 5
- POST /files/{path} - creates the file  # commit 7

## Types of responses

- 200 OK
- 201 Created  # commit 8
- 400 Bad request
- 404 Not found