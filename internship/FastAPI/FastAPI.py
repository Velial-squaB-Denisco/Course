import uvicorn
from fastapi import FastAPI

def main():
    uvicorn.run("FastAPI:app", host = '0.0.0.0', port = 8000, reload = True, workers = 3) 

if __name__ == '__main__':
    main()