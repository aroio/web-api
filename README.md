# ABACUS Aroio API for Webinterfaces and App-Connections

## Setup

Start virtual python environment if you don't have python3 running

setup:
```
$ python3 -m venv .
```
activate:
``` 
$ source venv/bin/activate
```
deactivate:
``` 
$ deactivate
```

### Requirements
All requirements can be installed with pip. Required dependencies are:
- [`fastapi`](https://fastapi.tiangolo.com/)
- [`uvicorn`](https://www.uvicorn.org/)
- [`pyyaml`](https://pyyaml.org/wiki/PyYAMLDocumentation)

## Run API:
To start the ASGI server via uvicorn run
``` 
$ uvicorn main:aroio_api --reload
```
or
```
$ scripts/startApi.sh
```
