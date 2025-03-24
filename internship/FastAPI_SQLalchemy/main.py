#uvicorn main:app --reload
import sqlalchemy
import uvicorn

from fastapi import FastAPI

app = FastAPI()

books = [
    {
        "id": 1,
        "title": "Асинхронность в Python",
        "author": "Маттью",
    },
    {
        "id": 2,
        "title": "Python",
        "author": "Митч",
    }
]

@app.get("/", summary="Main", tags=["Root"])
def Home():
    return "Hello world"

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)