# Hello world za FastAPI.
from fastapi import FastAPI
#Swagger dokumentacija je avtomatsko ustvarjena na /docs.
app = FastAPI()

@app.get("/")
async def hello():
    return {"Message": "Hello World!"}
@app.get("/hello")
async def hello(name: str):
    return {"Message": f"Hello, {name}! This is a way to pass parameters!"}
@app.get("/hello/{name}")
async def hello_name(name: str):
    return {"Message": f"Hello, {name}! This is another way to pass parameters!"}
