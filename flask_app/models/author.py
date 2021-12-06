from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book

class Author:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.favorite_books = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM authors;"
        authors_from_db = connectToMySQL('books_schema').query_db(query)
        authors = []
        for author in authors_from_db:
            authors.append(cls(author))
        return authors

    @classmethod
    def save(cls, data):
        query = "INSERT INTO authors(name) VALUES (%(name)s);"
        result = connectToMySQL('books_schema').query_db(query, data)
        return result

    @classmethod
    def get_author_with_favorites(cls, data):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON favorites.book_id = books.id WHERE authors.id = %(id)s;"
        results = connectToMySQL('books_schema').query_db(query, data)
        one_author = cls(results[0])
        for one_result in results:
            one_author.favorite_books.append(book.Book({
                'id': one_result['books.id'],
                'title': one_result['title'],
                'num_of_pages': one_result['num_of_pages'],
                'created_at': one_result['books.created_at'],
                'updated_at': one_result['books.updated_at']
            }))
        return one_author

    @classmethod
    def instert_into_favorites(cls, data):
        query = "INSERT INTO favorites (author_id, book_id) Values (%(author_id)s, %(book_id)s);"
        result = connectToMySQL('books_schema').query_db(query, data)
        return