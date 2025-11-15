import sqlite3
from .interfaces.IBookRepository import IBookRepository



class SqliteBookRepository(IBookRepository):
    def __init__(self, db_path='library.db'):
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.create_table()
        
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER NOT NULL
            )
        """)
        self.connection.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM books")
        data = self.cursor.fetchall()
        print("ID | Название книги | Автор | Год издания:")
        for i in range(len(data)):
            print(f"{data[i][0]} | {data[i][1]} | {data[i][2]} | {data[i][3]}")
        return data
    def add(self, title, author, year):
        self.cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)",(title,author,year))
        self.connection.commit()
        print(f"Книга '{title}' успешно добавлена!")
    
    def update(self, book_id, title, author, year):
        self.cursor.execute("UPDATE books SET title = ?, author = ?, year = ? WHERE id = ?",(title,author,year,book_id))
        self.connection.commit()
        
    
    def delete(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?",(book_id,))
        self.connection.commit()
        print(f"Книга с ID {book_id} успешно удалена!")
        
    
    def find_by_id(self, book_id):
        self.cursor.execute("SELECT * FROM books WHERE id = ?",(book_id,))
        data = self.cursor.fetchall()
        if len(data) != 0:
            pass
        else:
            print(f"Нету книги с ID {book_id}")
        return data
    
    def find_by_author(self, author_name):
        self.cursor.execute("SELECT * FROM books WHERE author = ?",(author_name,))
        data = self.cursor.fetchall()
        if len(data) != 0:
            pass
        else:
            print(f"Нету книг с автором '{author_name}'")
        return data
    
    def close(self):
        self.connection.close()