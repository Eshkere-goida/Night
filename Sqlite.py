import abc
import mysql.connector
import sqlite3

class IBookStorage(abc.ABC):
    @abc.abstractmethod
    def get_all(self):
        pass
    
    @abc.abstractmethod
    def add(self, title, author, year):
        pass
    
    @abc.abstractmethod
    def update(self, book_id, title, author, year):
        pass
    
    @abc.abstractmethod
    def delete(self, book_id):
        pass
    
    @abc.abstractmethod
    def find_by_id(self, book_id):
        pass
    
    @abc.abstractmethod
    def find_by_author(self, author):
        pass


class MySQLBookStorage(IBookStorage):
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
        if len(data) != 0:
            print("ID | Название книги | Автор | Год издания:")
            for book in data:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
        else:
            print(f"Нету книги с ID {book_id}")
        return data
    
    def find_by_author(self, author_name):
        sql_query = "SELECT * FROM books WHERE author = %s"
        data_tuple = (author_name,)
        self.cursor.execute(sql_query, data_tuple)
        data = self.cursor.fetchall()
        if len(data) != 0:
            print("ID | Название книги | Автор | Год издания:")
            for book in data:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
        else:
            print(f"Нету книг с автором '{author_name}'")
        return data
    
    def close(self):
        self.cursor.close()
        self.connection.close()


db = MySQLBookStorage(
    host="localhost",
    user="root",
    password="admin",
    database="test"
)
    
        
db.cursor.execute("TRUNCATE TABLE books")
db.connection.commit()
        
db.add("Война и мир", "Лев Толстой", 1869)
db.add("Анна Каренина", "Лев Толстой", 1877)
db.add("Преступление и наказание", "Федор Достоевский", 1866)
db.add("Идиот", "Федор Достоевский", 1869)
db.add("Отцы и дети", "Иван Тургенев", 1862)      

print("\n--- Все книги ---")
db.get_all()
        
print("\n--- Найти по автору ---")
db.find_by_author("Лев Толстой")
        
print("\n--- Найти по ID ---")
db.find_by_id(1)
        
print("\n--- Обновить книгу ---")
db.update(1, "Отцы и дети", "Иван Тургенев", 1926)
        
print("\n--- Все книги ---")
db.get_all()
        
db.close()


print("\n-------------------------------------------\n")


class Sqlite3BookStorage(IBookStorage):
    def __init__(self, db_path='books.db'):
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
        print(f"Книга с ID {book_id} успешно обновлена!")
        
    
    def delete(self, book_id):
        self.cursor.execute("DELETE FROM books WHERE id = ?",(book_id,))
        self.connection.commit()
        print(f"Книга с ID {book_id} успешно удалена!")
        
    
    def find_by_id(self, book_id):
        self.cursor.execute("SELECT * FROM books WHERE id = ?",(book_id,))
        data = self.cursor.fetchall()
        if len(data) != 0:
            print("ID | Название книги | Автор | Год издания:")
            for book in data:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
        else:
            print(f"Нету книги с ID {book_id}")
        return data
    
    def find_by_author(self, author_name):
        self.cursor.execute("SELECT * FROM books WHERE author = ?",(author_name,))
        data = self.cursor.fetchall()
        if len(data) != 0:
            print("ID | Название книги | Автор | Год издания:")
            for book in data:
                print(f"{book[0]} | {book[1]} | {book[2]} | {book[3]}")
        else:
            print(f"Нету книг с автором '{author_name}'")
        return data
    
    def close(self):
        self.connection.close()

storage = Sqlite3BookStorage("books.db")


storage.cursor.execute("DELETE FROM books")
storage.connection.commit()  


storage.add("Война и мир", "Лев Толстой", 1869)
storage.add("Анна Каренина", "Лев Толстой", 1877)
storage.add("Преступление и наказание", "Федор Достоевский", 1866)
storage.add("Идиот", "Федор Достоевский", 1869)
storage.add("Отцы и дети", "Иван Тургенев", 1862)



print("Все книги после добавления:")
books = storage.get_all()

    
print("\nПоиск книг Толстого:")
storage.find_by_author("Толстой")

    

print("\nПоиск книги с ID=3:")
storage.find_by_id(3)

    
print("\nОбновление книги с ID=1:")
storage.update(1, "Мастер и Маргарита (полная версия)", "Михаил Булгаков", 1967)

    
print("\nУдаление книги с ID=4:")
storage.delete(4)
books_after_delete = storage.get_all()
print(f"  Осталось книг: {len(books_after_delete)}")


storage.close()



print("\n-------------------------------------------\n")



class ListBookStorage:
    def __init__(self):
        self.books = []
        self.next_id = 1

    def get_all(self):
        print("Все книги в хранилище:")
        if not self.books:
            print("  Хранилище пусто")
        else:
            for book in self.books:
                print(f"  {book['id']}: '{book['title']}' - {book['author']} ({book['year']})")
        return self.books.copy()

    def add(self, title, author, year):
        book = {
            'id': self.next_id,
            'title': title,
            'author': author,
            'year': year
        }
        self.books.append(book)
        self.next_id += 1
        print(f"Книга '{title}' успешно добавлена! (ID: {book['id']})")
        return True

    def update(self, book_id, title, author, year):
        for book in self.books:
            if book['id'] == book_id:
                book['title'] = title
                book['author'] = author
                book['year'] = year
                print(f"Книга с ID {book_id} успешно обновлена!")
                return True
        print(f"Книга с ID {book_id} не найдена!")
        return False

    def delete(self, book_id):
        for i in range(len(self.books)):
            if book['id'] == book_id:
                deleted_title = book['title']
                del self.books[i]
                print(f"Книга '{deleted_title}' (ID: {book_id}) успешно удалена!")
                return True
        print(f"Книга с ID {book_id} не найдена!")
        return False

    def find_by_id(self, book_id):
        for book in self.books:
            if book['id'] == book_id:
                print(f"Найдена книга: '{book['title']}' - {book['author']} ({book['year']})")
                return book
        print(f"Книга с ID {book_id} не найдена!")
        return None

    def find_by_author(self, author_name):
        found_books = []
        for book in self.books:
            if author_name.lower() in book['author'].lower():
                found_books.append(book)
        
        if found_books:
            print(f"Книги автора '{author_name}':")
            for book in found_books:
                print(f"  {book['id']}: '{book['title']}' ({book['year']})")
        else:
            print(f"Книги автора '{author_name}' не найдены")
        
        return found_books

storage = ListBookStorage()

storage.add("Война и мир", "Лев Толстой", 1869)
storage.add("Анна Каренина", "Лев Толстой", 1877)
storage.add("Преступление и наказание", "Федор Достоевский", 1866)
storage.add("Идиот", "Федор Достоевский", 1869)
storage.add("Отцы и дети", "Иван Тургенев", 1862)




storage.get_all()



print("\nПоиск книг Толстого:")
tolstoy_books = storage.find_by_author("Толстой")



print("\nПоиск книги с ID=3:")
book = storage.find_by_id(3)


print("\nОбновление книги с ID=1:")
storage.update(1, "Мастер и Маргарита", "Михаил Булгаков", 1967)


print("\nРезультат обновления:")
storage.find_by_id(1)

print("\nУдаление книги с ID=4:")
storage.delete(4)



books_after_delete = storage.get_all()
print(f"Всего книг осталось: {len(books_after_delete)}")

