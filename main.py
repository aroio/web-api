from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import settings, oauth

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

aroio_api.include_router(settings.router)
aroio_api.include_router(oauth.router)
