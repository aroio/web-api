#!/usr/bin/env python3

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import (
    aroio_routers,
    languages_routers,
    oauth_routers,
    measurement_routers
)

###############
# Setup
###############

aroio_api = FastAPI()
aroio_api.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
        "http://localhost:4200",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aroio_api.include_router(aroio_routers.router)
aroio_api.include_router(oauth_routers.router)
aroio_api.include_router(languages_routers.router)
aroio_api.include_router(measurement_routers.router)

if __name__ == "__main__":
    uvicorn.run(aroio_api, host="0.0.0.0", port=8000)
