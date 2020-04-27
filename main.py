import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import DataSource
from routers import settings

###############
# Setup
###############
aroio_api = FastAPI()
datasource = DataSource()

if __name__ == "__main__":
    
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
    uvicorn.run(aroio_api, host="127.0.0.1", port=8000)