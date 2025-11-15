from repositories.SqliteBookRepository import SqliteBookRepository
from repositories.MySqlBookRepository import MySqlBookRepository
from repositories.MemoryBookRepository import MemoryBookRepository

from services.LibraryService import LibraryService
from controllers.LibraryController import LibraryController


def main():
    
    
    sqlite_repo = SqliteBookRepository()
    
    
    mysql_repo = MySqlBookRepository(
        host="localhost", 
        user="root", 
        password="admin",
        database="test"
    )
    
    memory_repo = MemoryBookRepository()

    
    all_repositories = {
        'sqlite': sqlite_repo,
        'mysql': mysql_repo,
        'memory': memory_repo
    }


    service = LibraryService(repositories=all_repositories)

    controller = LibraryController(service=service)


    controller.run()



if __name__ == "__main__":
    main()







# db = MySQLBookStorage(
#     host="localhost",
#     user="root",
#     password="admin",
#     database="test"
# )
    
        
# db.cursor.execute("TRUNCATE TABLE books")
# db.connection.commit()
        
# db.add("Война и мир", "Лев Толстой", 1869)
# db.add("Анна Каренина", "Лев Толстой", 1877)
# db.add("Преступление и наказание", "Федор Достоевский", 1866)
# db.add("Идиот", "Федор Достоевский", 1869)
# db.add("Отцы и дети", "Иван Тургенев", 1862)      

# print("\n--- Все книги ---")
# db.get_all()
        
# print("\n--- Найти по автору ---")
# db.find_by_author("Лев Толстой")
        
# print("\n--- Найти по ID ---")
# db.find_by_id(1)
        
# print("\n--- Обновить книгу ---")
# db.update(1, "Отцы и дети", "Иван Тургенев", 1926)
        
# print("\n--- Все книги ---")
# db.get_all()
        
# db.close()


#-------------------------------------------




# storage = Sqlite3BookStorage("books.db")


# storage.cursor.execute("DELETE FROM books")
# storage.connection.commit()  


# storage.add("Война и мир", "Лев Толстой", 1869)
# storage.add("Анна Каренина", "Лев Толстой", 1877)
# storage.add("Преступление и наказание", "Федор Достоевский", 1866)
# storage.add("Идиот", "Федор Достоевский", 1869)
# storage.add("Отцы и дети", "Иван Тургенев", 1862)



# print("Все книги после добавления:")
# books = storage.get_all()

    
# print("\nПоиск книг Толстого:")
# storage.find_by_author("Толстой")

    

# print("\nПоиск книги с ID=3:")
# storage.find_by_id(3)

    
# print("\nОбновление книги с ID=1:")
# storage.update(1, "Мастер и Маргарита (полная версия)", "Михаил Булгаков", 1967)

    
# print("\nУдаление книги с ID=4:")
# storage.delete(4)
# books_after_delete = storage.get_all()
# print(f"  Осталось книг: {len(books_after_delete)}")


# storage.close()



#-------------------------------------------




# storage = ListBookStorage()

# storage.add("Война и мир", "Лев Толстой", 1869)
# storage.add("Анна Каренина", "Лев Толстой", 1877)
# storage.add("Преступление и наказание", "Федор Достоевский", 1866)
# storage.add("Идиот", "Федор Достоевский", 1869)
# storage.add("Отцы и дети", "Иван Тургенев", 1862)




# storage.get_all()



# print("\nПоиск книг Толстого:")
# tolstoy_books = storage.find_by_author("Толстой")



# print("\nПоиск книги с ID=3:")
# book = storage.find_by_id(3)


# print("\nОбновление книги с ID=1:")
# storage.update(1, "Мастер и Маргарита", "Михаил Булгаков", 1967)


# print("\nРезультат обновления:")
# storage.find_by_id(1)

# print("\nУдаление книги с ID=4:")
# storage.delete(4)



# books_after_delete = storage.get_all()
# print(f"Всего книг осталось: {len(books_after_delete)}")