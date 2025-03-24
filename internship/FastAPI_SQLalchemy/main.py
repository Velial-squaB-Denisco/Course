import sqlalchemy

from fastapi import FastAPI

app = FastAPI()

def root():
    return "hello"

@app.get("/")
def read_root():
    return {"Hello": "World"}