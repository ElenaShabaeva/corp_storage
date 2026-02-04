from fastapi import FastAPI
from database.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from controllers.routers import router
import logging
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format="%(name)s %(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

app = FastAPI()
app.include_router(router)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
