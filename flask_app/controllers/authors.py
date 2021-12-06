from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_app.models.author import Author
from flask_app.models.book import Book

@app.route('/authors')
def authors():
    all_authors = Author.get_all()
    return render_template('authors.html', all_authors=all_authors)

@app.route('/addNewAuthor', methods=['POST'])
def add_new_author():
    data = {
        'name': request.form['name']
    }
    Author.save(data)
    return redirect('/authors')

@app.route('/author/<int:author_id>')
def show_author(author_id):
    data = {
        'id': author_id
    }
    one_author = Author.get_author_with_favorites(data)
    all_books = Book.get_all()
    for authors_book in one_author.favorite_books:
        for book in all_books:
            if authors_book.title == book.title:
                all_books.remove(book)
    return render_template('author_show.html', author=one_author, all_books=all_books)

@app.route('/addToAuthorsFavorites', methods=['POST'])
def add_to_authors_favorites():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    Author.instert_into_favorites(data)
    return redirect(f"/author/{data['author_id']}")