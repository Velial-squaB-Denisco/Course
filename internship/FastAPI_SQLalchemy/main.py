# #uvicorn main:app --reload
# import uvicorn
# from pydantic import BaseModel
# from fastapi import FastAPI, HTTPException

# app = FastAPI()

# books = [
#     {
#         "id": 1,
#         "title": "Асинхронность в Python",
#         "author": "Маттью",
#     },
#     {
#         "id": 2,
#         "title": "Python",
#         "author": "Митч",
#     }
# ]

# @app.get("/books")
# def read_books():
#     return books

# @app.get("/books/{book_id}")
# def get_book(book_id: int):
#     for book in books:
#         if book["id"] == book_id:
#             return book
        
#         raise HTTPException(status_code=404, detail="Book not found")
    
# class NewBook(BaseModel):
#     title: str
#     author: str

# @app.post("/books")
# def create_books(new_book: NewBook):
#     books.append({
#         "id": len(books) + 1,
#         "title": new_book.title,
#         "author": new_book.author
#     })
#     return {"Succes": True, "message": "Succes"}


# if __name__ == '__main__':
#     uvicorn.run("main:app", reload=True)

# import uvicorn
# from fastapi import FastAPI
# from pydantic import BaseModel, Field, EmailStr

# app = FastAPI()
# data = {
#         "email": "abc@mail.ru",
#         "bio": "Асинхронность в Python",
#         "age": 14,
#     }

# class UserSchema(BaseModel):
#     email: EmailStr
#     bio: str | None = Field(max_length=1000)

# class UserAgeSchema(UserSchema):
#     age: int = Field(ge=0, le=130)

# users = []

# @app.post("/users")
# def add_user(user: UserAgeSchema):
#     users.append(user)
#     return {"succes"}

# @app.get("/users") 
# def get_user() -> list [UserAgeSchema]:
#     return users

# print(UserAgeSchema(**data))

# if __name__ == "__main__":
#     uvicorn.run("main:app", reload=True)

from typing import Annotated

import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

app = FastAPI()

engine = create_async_engine('sqlite+aiosqlite:///books.db')

# with engine.connect() as conn:
#     conn.execute("""""")

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessinDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class BookModel(Base):
    __tablename__ = "Books"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

class BookAddSchema(BaseModel):
    title: str
    author: str

class BookASchema(BookAddSchema):
    id: int

@app.post("/books")
async def add_book(book: BookAddSchema, session: SessinDep):
    new_book = BookModel(
        title = book.title,
        author = book.author
    )
    session.add(new_book)
    await session.commit()
    return {"ok"}

@app.get("/books")
async def get_book(session: SessinDep):
    qwery = select(BookModel)
    res = await session.execute(qwery)
    return res.all()

if __name__ == "__main__":
    uvicorn.run("main:app")