from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.book import Book
from flask_app.models.author import Author


@app.route('/books')
def books():
    all_books = Book.get_all()
    return render_template('books.html', all_books=all_books)

@app.route('/addNewBook', methods=['POST'])
def add_new_book():
    data = {
        'title': request.form['title'],
        'num_of_pages': request.form['num_of_pages']
    }
    Book.save(data)
    return redirect('/books')

@app.route('/book/<int:book_id>')
def show_book(book_id):
    data = {
        'id': book_id
    }
    book = Book.get_book_with_authors(data)
    all_authors = Author.get_all()
    for books_author in book.authors:
        for one_author in all_authors:
            if books_author.name == one_author.name:
                all_authors.remove(one_author)
    return render_template('book_show.html', book=book, all_authors=all_authors)

@app.route('/addBooksFavorites', methods=['POST'])
def add_books_favorites():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.instert_into_favorites(data)
    return redirect(f"/book/{data['book_id']}")