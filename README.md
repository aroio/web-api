# ABACUS Aroio API for Webinterfaces and App-Connections

## Setup

Start virtual python environment if you don't have python3 running

setup:
```bash
$ python3 -m venv venv
$ pip install -r requirements.txt
```
activate:
```bash 
$ source venv/bin/activate
```
deactivate:
```bash
$ deactivate
```

### Requirements
All requirements can be installed with pip. Required dependencies are:
- [`fastapi`](https://fastapi.tiangolo.com/)
- [`uvicorn`](https://www.uvicorn.org/)
- [`pyyaml`](https://pyyaml.org/wiki/PyYAMLDocumentation)
- [`PyJWT`](https://pyjwt.readthedocs.io/en/latest/)
- [`python-multipart`](https://github.com/andrew-d/python-multipart)


## Run API:
To start the ASGI server via uvicorn run
```bash
$ uvicorn main:aroio_api --reload
```
or
```bash
$ ./scripts/startApi.sh
```


# AroioOS Linux Build

use google cloud platform with an nice and powerful setup with a shitload of RAM and do your AroioOS Kernel Build via ssh on a virtual maschine.

```bash
$ sudo apt install -y sed make binutils build-essential gcc g++ bash patch gzip bzip2 perl tar cpio python unzip rsync file bc wget git screen flex libssl-dev jq
$ git clone --recurse-submodules https://github.com/aroio/aroio-ng.git
$ cd aroio-ng
```

use Instructions on https://github.com/aroio/aroio-ng and do your changes in some feature-branch
