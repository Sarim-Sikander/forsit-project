import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import Inventory, Sales

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(docs_url="/home", include_in_schema=True)

origins: list[str] = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(Sales.router)
app.include_router(Inventory.router)
