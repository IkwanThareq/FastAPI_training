from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status
from typing import Optional

app = FastAPI()
#class buku

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    publish_date: int

    def __init__(self, id, title, author, description, rating, publish_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.publish_date = publish_date

# create class using pydantic basemodel for validate the parameter 
# to input by user
# class di bawah ini itu object type pydantic karena pakai BaseModel
# optional buat kasih tahu ini bisa ada nilainya atau tdk
class BookRequest(BaseModel):
    id : Optional[int] = Field(title= 'there is no need a title')
    title: str = Field(min_length= 3)
    author: str = Field(min_length=1)
    description: str = Field(min_length= 1, max_length=100)
    rating: int = Field(gt= 0, lt= 6)
    publish_date : int = Field(gt = 1999, lt=2031)

    # di bawah ini untuk config pydantic
    class Config:
        json_schema_extra = {
            'example': {
                'id': 0,
                'title': 'A new Book',
                'author': 'coding with tarso',
                'description': 'coding mantop',
                'rating': 5,
                'publish_date': 2001
            }
        }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2021),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2021),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2022),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2022),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2023),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1,2024)
]

@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

# This below API endpoint is for fethcing data book by id
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
#NOTE adding data validation in path paramenters
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    # this below is to put http exception if there is no book id that match with the data 
    raise HTTPException(status_code=404, detail='items not found')
        
# api for filter by book rating , using query parameter
@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    #dibawah ini bikin empyt array buat masukin list by rating
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


#create post request
@app.post("/create_book", status_code=status.HTTP_201_CREATED)
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

# this below is put request method, untuk update datanya yang ada 
# NOTE API put ini blm ada exception handling, jadi kalau di kasih ID yg gk ada itu requestnya masih 200 dan berhasil
# tapi itu masih salah, next akan diperbaiki
@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    #NOTE this code below will put check with httpException
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

# NOTE API below is delete method 
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt = 0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')

#NOTE this API below is to get the data book by query parameter using publish_date
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
async def getBookByPublishDate(book_publish: int = Query(gt = 1999, lt=2031)):
    book_publish_date = []
    for book in BOOKS:
        if book.publish_date == book_publish:
            book_publish_date.append(book)
    return book_publish_date