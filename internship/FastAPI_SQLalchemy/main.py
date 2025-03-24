#uvicorn main:app --reload
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData

import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()

engine = create_engine('sqlite:///books.db') 
books = Table('books', MetaData,
              Column('id', Integer, primary_key=True),
              Column('title', String),
              Column('author', String))
MetaData.create_all(engine)

@app.get("/books")
def read_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
        
        raise HTTPException(status_code=404, detail="Book not found")
    
class NewBook(books):
    Column('title', String),
    Column('author', String)

@app.post("/books")
def create_books(new_book: NewBook):
    books.update({ Column('title', String),
    Column('author', String)})


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)