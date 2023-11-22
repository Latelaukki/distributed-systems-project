from typing import Union
from fastapi import FastAPI, Request
import uuid

SERVER_ID = uuid.uuid4()

app = FastAPI()

@app.get("/")
def read_root():
   return {"Hello": "World"}

@app.get("/get-maze")
def main():
    return {f"Returned maze |---|--|----| from {SERVER_ID}"}

@app.get('/get-server')
def main(request: Request):
    host_url = request.headers.get('host')
    return {f"This is server {host_url}"}