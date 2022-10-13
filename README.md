# UE-AD-A1-REST

TP Flask, REST, OpenAPI, gRPC and GraphQL

## How to dockerize ?

Run ```docker-compose up -d```
This will launch all the services on their respective ports
To launch test run ```python3 test/main.py```
All other tests need to be done by hand

## Services list :

| Service  | Port |
|----------|------|
| movie    | 3001 |
| booking  | 3002 |
| user     | 3004 |
| showtime | 3003 |

WARNING : Put your IMDB_KEY in a .env, otherwise you will not be able to fetch from IMDB's API

All services communicate throught the docker default network, and use the respective container hostname with their
respective port

BOËLLE Octave
GLOCK Matteo