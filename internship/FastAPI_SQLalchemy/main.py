#uvicorn main:app --reload
import sqlalchemy

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return "Hello world"
