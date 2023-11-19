from typing import Union
from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
def read_root():
   return {"Hello": "World"}

@app.get("/get-maze")
def main():
    return {"Returned maze |---|--|----|"}

@app.get('/get-server')
def main(request: Request):
    host_url = request.headers.get('host')
    return {f"This is server {host_url}"}