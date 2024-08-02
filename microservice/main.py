from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from crud import product_crud
from db import async_session_maker


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
async def index():
    return JSONResponse(content={"message": "Hello"})


@app.get('/products')
async def get_products():
    session = async_session_maker()
    products = await product_crud.get_paginated(session=session, )
    await session.close()
    return products
