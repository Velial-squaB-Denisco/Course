import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base

Base.metadata.create_all(bild = engine)

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run("FastAPI:app", host = '0.0.0.0', port = 8000, reload = True, workers = 3)