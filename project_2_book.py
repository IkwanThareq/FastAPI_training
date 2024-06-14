from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()
#class buku

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

# create class using pydantic basemodel for validate the parameter 
# to input by user
# class di bawah ini itu object type pydantic karena pakai BaseModel
# optional buat kasih tahu ini bisa ada nilainya atau tdk
class BookRequest(BaseModel):
    id : Optional[int] = Field(title='there is no need a title')
    title: str = Field(min_length= 3)
    author: str = Field(min_length=1)
    description: str = Field(min_length= 1, max_length=100)
    rating: int = Field(gt= 0, lt= 6)

    # di bawah ini untuk config pydantic
    class Config:
        json_schema_extra = {
            'example': {
                'id': 0,
                'title': 'A new Book',
                'author': 'coding with tarso',
                'description': 'coding mantop',
                'rating': 5
            }
        }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1)
]

@app.get("/books")
async def read_all_books():
    return BOOKS

#create post request
@app.post("/create_book")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    
    BOOKS.append(find_book_id(new_book))

def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    #di bawah ini itu ternary operator 
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book