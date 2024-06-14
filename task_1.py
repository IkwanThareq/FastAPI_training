from fastapi import FastAPI, Body

app = FastAPI()

buku = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

# @app.get("/books")
# async def read_all_book():
#     return BOOKS

@app.get("/books/book_all_from_author/{author_book}")
async def list_author_book(author_book: str):
    author_book_res = []
    for i in buku : 
        if i.get('author').casefold() == author_book.casefold():
            author_book_res.append(i)
    return author_book_res
        