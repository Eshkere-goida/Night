from .interfaces.IBookRepository import IBookRepository
import mysql.connector

class MySqlBookRepository(IBookRepository):
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        self.create_table()
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books(
                book_id INT PRIMARY KEY AUTO_INCREMENT,
                title VARCHAR(100),
                author VARCHAR(100),
                year INT
            )
        """)
        self.connection.commit()
    
    def get_all(self):
        self.cursor.execute("SELECT * FROM books")
        data = self.cursor.fetchall()
        print("ID | Название книги | Автор | Год издания:")
        for book in data:
            print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
        return data
    
    def add(self, title, author, year):
        sql_query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
        data_tuple = (title, author, year)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"Книга '{title}' успешно добавлена!")
    
    def update(self, book_id, title, author, year):
        sql_query = "UPDATE books SET title = %s, author = %s, year = %s WHERE book_id = %s"
        data_tuple = (title, author, year, book_id)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"Книга с ID {book_id} успешно обновлена!")
        
    
    def delete(self, book_id):
        sql_query = "DELETE FROM books WHERE book_id = %s"
        data_tuple = (book_id,)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"Книга с ID {book_id} успешно удалена!")
        
    
    def find_by_id(self, book_id):
        sql_query = "SELECT * FROM books WHERE book_id = %s"
        data_tuple = (book_id,)
        self.cursor.execute(sql_query, data_tuple)
        data = self.cursor.fetchall()
        return data
    
    def find_by_author(self, author_name):
        sql_query = "SELECT * FROM books WHERE author = %s"
        data_tuple = (author_name,)
        self.cursor.execute(sql_query, data_tuple)
        data = self.cursor.fetchall()
        return data
    
    def close(self):
        self.cursor.close()
        self.connection.close()