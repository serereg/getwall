# GETWALL

A REST API that returns the combined posts and comments provided from
these two endpoints, while caching the responses:
"https://jsonplaceholder.typicode.com/posts"
"https://jsonplaceholder.typicode.com/comments"

This app was based on
https://python-dependency-injector.ets-labs.org/examples/fastapi-redis.html
Swagger is here: <http://localhost:8000/docs>

FastAPI + Redis + Dependency Injector Example

This is a [FastAPI](https://docs.python.org/3/library/asyncio.html) +
[Redis](https://redis.io/) + [Dependency
Injector](https://python-dependency-injector.ets-labs.org/) example
application.

## Run

Build the Docker image:

``` bash
docker-compose build
```

Run the docker-compose environment:

``` bash
docker-compose up
```

The output should be something like:

``` 
fastapi-redis-redis-1    | 1:C 19 Dec 2022 02:33:02.484 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
fastapi-redis-redis-1    | 1:C 19 Dec 2022 02:33:02.484 # Redis version=7.0.5, bits=64, commit=00000000, modified=0, pid=1, just started
fastapi-redis-redis-1    | 1:C 19 Dec 2022 02:33:02.484 # Configuration loaded
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.485 * monotonic clock: POSIX clock_gettime
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.485 * Running mode=standalone, port=6379.
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.485 # Server initialized
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.487 * Loading RDB produced by version 7.0.5
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.487 * RDB age 58 seconds
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.487 * RDB memory usage when created 0.85 Mb
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.487 * Done loading RDB, keys loaded: 0, keys expired: 0.
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.487 * DB loaded from disk: 0.000 seconds
fastapi-redis-redis-1    | 1:M 19 Dec 2022 02:33:02.488 * Ready to accept connections
fastapi-redis-example-1  | INFO:     Started server process [1]
fastapi-redis-example-1  | INFO:     Waiting for application startup.
fastapi-redis-example-1  | INFO:     Application startup complete.
fastapi-redis-example-1  | INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
fastapi-redis-example-1  | INFO:     172.18.0.1:63998 - "GET / HTTP/1.1" 200 OK
fastapi-redis-example-1  | INFO:     172.18.0.1:63998 - "GET /favicon.ico HTTP/1.1" 404 Not Found
fastapi-redis-example-1  | INFO:     172.18.0.1:63998 - "GET / HTTP/1.1" 200 OK
fastapi-redis-example-1  | INFO:     172.18.0.1:63998 - "GET / HTTP/1.1" 200 OK
```

## Test

This application comes with the unit tests.

To run the tests do:

``` bash
docker-compose run --rm getwall pytest tests --cov=getwall
```

The output should be something like:

``` 
...

----------- coverage: platform linux, python 3.9 -----------
Name                          Stmts   Miss  Cover
-------------------------------------------------
fastapiredis/__init__.py          0      0   100%
fastapiredis/application.py      14      0   100%
fastapiredis/containers.py        6      0   100%
fastapiredis/redis.py             7      4    43%
fastapiredis/services.py          7      3    57%
fastapiredis/tests.py            18      0   100%
-------------------------------------------------
TOTAL                            52      7    87%
```
