#uvicorn main:app --reload
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.orm import sessionmaker, Session

import uvicorn
from fastapi import FastAPI, HTTPException, Depends

from pydantic import BaseModel

app = FastAPI()

# Создание модуля для метаданных
metadata = MetaData()

# Инициализация базы данных
engine = create_engine('sqlite:///books.db')

# Определение таблицы "books"
books = Table('books', metadata,
              Column('id', Integer, primary_key=True),
              Column('title', String),
              Column('author', String))

# Создание таблиц в базе данных
metadata.create_all(engine)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/books")
def read_books(db: Session = Depends(get_db)):
    return db.execute(books.select()).fetchall()

@app.get("/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    query = books.select().where(books.c.id == book_id)
    book = db.execute(query).fetchone()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

class NewBook(BaseModel):
    title: str
    author: str

@app.post("/books")
def create_book(new_book: NewBook, db: Session = Depends(get_db)):
    new_book_data = {
        "id": len(books) + 1,
        "title": new_book.title,
        "author": new_book.author
    }
    db.execute(books.insert().values(**new_book_data))
    db.commit()
    return new_book_data

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)