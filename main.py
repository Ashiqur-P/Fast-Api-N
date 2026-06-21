from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import engine, Base

import models # ⚠️ এই লাইনটি অবশ্যই থাকতে হবে

from routers import products, books, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(products.router)
app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI Application"}