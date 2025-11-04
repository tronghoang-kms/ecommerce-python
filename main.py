from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.connection import init_db
from api.v1.api import api_router
from core.config import settings
from middlewares.error_handling import (
    http_exception_handler, 
    document_not_found_handler,
    unhandled_exception_handler
)
from beanie.exceptions import DocumentNotFound
from starlette.exceptions import HTTPException as StarletteHTTPException


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    await init_db()
    yield
    print("Shutting down...")

app = FastAPI(
    title="E-Commerce API",
    description="e-commerce with FastAPI and Beanie.",
    version="0.1.0",
    lifespan=lifespan
)


app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(DocumentNotFound, document_not_found_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)



app.include_router(api_router, prefix="/api/v1")

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": f"Welcome to the E-Commerce API! View docs at /docs"}
