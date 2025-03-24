#uvicorn main:app --reload
import sqlalchemy
import uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.get("/", summary="Main", tags=["Root"])
def Home():
    return "Hello world"

if __name__ == '__main__':
    uvicorn.run("main:app")