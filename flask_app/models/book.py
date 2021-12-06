from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

class Book:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []


    @classmethod
    def save(cls, data):
        query = "INSERT INTO books (title, num_of_pages) VALUES(%(title)s, %(num_of_pages)s);"
        burger_id = connectToMySQL('books_schema').query_db(query, data)
        return burger_id

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM books"
        books_from_db = connectToMySQL('books_schema').query_db(query)
        books = []
        for book in books_from_db:
            books.append(cls(book))
        return books

    @classmethod
    def get_book_with_authors(cls, data):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON favorites.author_id = authors.id WHERE books.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)
        one_book = cls(results[0])
        for one_result in results:
            one_book.authors.append(author.Author({
                'id': one_result['authors.id'],
                'name': one_result['name'],
                'created_at': one_result['authors.created_at'],
                'updated_at': one_result['authors.updated_at']
            }))
        return one_book