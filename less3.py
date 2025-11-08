import abc
import mysql.connector
import sqlite3



class IBookStorage(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        pass
    @abc.abstractmethod
    def add(self,title,author,year):
        pass
    @abc.abstractmethod
    def update(self,book_id,title,author,year):
        pass
    @abc.abstractmethod
    def delete(self,book_id):
        pass
    @abc.abstractmethod
    def find_by_id(self,book_id):
        pass
    @abc.abstractmethod
    def find_by_author(self,author):
        pass



connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="test"
)
cursor = connection.cursor()
cursor.execute("DELETE FROM books")



class MySQL(IBookStorage):
    def __init__(self,title,author,year):
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="test"
        )
        cursor = connection.cursor()
        self.title = title
        self.author = author
        self.year = year
        cursor.execute("""
                    CREATE TABLE IF NOT EXISTS books(
                        book_id INT PRIMARY KEY AUTO_INCREMENT,
                        title VARCHAR(100),
                        author VARCHAR(100),
                        year INT
                    )
            """)
        cursor.execute(f"INSERT INTO books(title,author,year) VALUES ('{title}','{author}',{year})")
        connection.commit()
        connection.close()
    def get_all(self):
        cursor.execute(f"SELECT * FROM books")
        data = cursor.fetchall()
        print("Название книги:   Автор:    Год издания:")
        for i in range(len(data)):
            print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
    def add(self,title,author,year):
        sql_query = "INSERT INTO books(title,author,year) VALUES (%s,%s,%s)"
        data_tuple = (title,author,year)
        cursor.execute(sql_query,data_tuple)
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        print("Название книги:   Автор:    Год издания:")
        for i in range(len(data)):
            print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
    def update(self, book_id, title, author, year):
        sql_query = "UPDATE books SET title = %s,author = %s,year = %s WHERE id = %s"
        data_tuple = (title,author,year,book_id)
        cursor.execute(sql_query,data_tuple)
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        print("Название книги:   Автор:    Год издания:")
        for i in range(len(data)):
            print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
    def delete(self, book_id):
        sql_query = "DELETE FROM books WHERE id = %s"
        data_tuple = (book_id,)
        cursor.execute(sql_query,data_tuple)
        cursor.execute("SELECT * FROM books")
        data = cursor.fetchall()
        print("Название книги:   Автор:    Год издания:")
        for i in range(len(data)):
            print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
        connection.commit()
    def find_by_id(self, book_id):
        sql_query = "SELECT * FROM books WHERE id = %s"
        data_tuple = (book_id,)
        cursor.execute(sql_query,data_tuple)
        data = cursor.fetchall()
        print("Название книги:   Автор:    Год издания:")
        print(f"{data[0][1]}, {data[0][2]}, {data[0][3]}")
    def find_by_author(self, author_name):
        sql_query = "SELECT * FROM books WHERE author = %s"
        data_tuple = (author_name,)
        cursor.execute(sql_query,data_tuple)
        data = cursor.fetchall()
        print("Название книги:   Автор:    Год издания:")
        print(f"{data[0][1]}, {data[0][2]}, {data[0][3]}")

    
db1 = MySQL('JJJ','KKK',1000)

db1.get_all()


