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

from pydantic import BaseModel, Field, EmailStr

data ={
        "email": "abc@mail.ru",
        "bio": "Асинхронность в Python",
        "age": 14,
    }

class UserSchema(BaseModel):
    email: EmailStr
    bio: str | None = Field(max_length=1000)
    age: int = Field(ge=0, le=130)

print(UserSchema(**data))