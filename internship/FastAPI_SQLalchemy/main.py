#uvicorn main:app --reload
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker

import uvicorn
from fastapi import FastAPI, HTTPException, Depends

from pydantic import BaseModel

app = FastAPI()

metadata = MetaData()
engine = create_engine('sqlite:///books.db') 
books = Table('books', metadata,
              Column('id', Integer, primary_key=True),
              Column('title', String),
              Column('author', String))

metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books")
def read_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
        
        raise HTTPException(status_code=404, detail="Book not found")
    
class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(new_book: NewBook, db=Depends(get_db)):
    new_book_data = {
        "title": new_book.title,
        "author": new_book.author
    }
    db.execute(books.insert().values(**new_book_data))
    db.commit()
    return new_book_data

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)