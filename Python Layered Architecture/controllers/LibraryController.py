
from services import LibraryService


class LibraryController:

    def __init__(self, service: LibraryService):
        
        self.service = service

    def run(self):
        
        print("Добро пожаловать в 'Чистую' Библиотеку!")
        
        
        if not self._select_storage():
            
            print("Выход из программы.")
            return

        
        self._main_menu()
        
        print("До свидания!")

    def _select_storage(self) -> bool:
        
        print("\n--- Выбор Хранилища Данных ---")
        print("1. SQLite (Файл 'library.db')")
        print("2. MySQL (Сервер 'localhost')")
        print("3. Memory (Список Python, для тестов)")
        print("q. Отмена / Выход") 

        while True:
            choice = input("Выберите (1, 2, 3 или q): ").strip().lower()
            repo_key = None
            
            if choice == '1':
                repo_key = 'sqlite'
            elif choice == '2':
                repo_key = 'mysql'
            elif choice == '3':
                repo_key = 'memory'
            elif choice == 'q':

              
                
                return False 
            else:
                print("Неверный выбор. Попробуйте еще раз.")
                continue 

        
            try:
                success = self.service.set_active_repository(repo_key)
                if success:
                    print(f"Хранилище '{repo_key}' успешно активировано.")
                    return True
                else:
                    print("Неизвестная ошибка сервиса.")
            
            except Exception as e:
                
                print(f"[!!!] Ошибка при активации '{repo_key}':")
                print(f"[!!!] {e}")
                print("Пожалуйста, проверьте подключение и попробуйте снова.")

            
        

    def _main_menu(self):
        while True:
            print("\n--- Главное Меню ---")
            print("1. Показать все книги")
            print("2. Добавить новую книгу")
            print("3. Обновить книгу (по ID)")
            print("4. Удалить книгу (по ID)")
            print("5. Найти книгу по ID")
            print("6. Найти книги по автору")
            print("7. СМЕНИТЬ ХРАНИЛИЩЕ") 
            print("8. Выход")
            
            choice = input("Выберите: ").strip()

            if choice == '1':
                self._get_all_books()
            elif choice == '2':
                self._add_book()
            elif choice == '3':
                self._update_book()
            elif choice == '4':
                self._delete_book()
            elif choice == '5':
                self._find_book_by_id()
            elif choice == '6':
                self._find_books_by_author()
            
        
            elif choice == '7':
                
                print("--- Переключение Хранилища ---")
                
                
                if self._select_storage():
                    print("Хранилище успешно сменено!")
                else:
                    print("Смена хранилища отменена, " \
                          "продолжаем работать со старым.")
                
                
                continue
            
            elif choice == '8': 
                break
            
            else:
                print("Неверный выбор.")

    
    def _get_all_books(self):
        print("\n--- Все книги ---")
        books = self.service.get_all_books()
        if not books:
            print("Библиотека пуста.")

    def _add_book(self):
        print("\n--- Добавить книгу ---")
        title = input("  Введите название: ")
        author = input("  Введите автора: ")
        year = input("  Введите год: ")
        try:
            self.service.add_book(title, author, year)
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")

    def _update_book(self):
        print("\n--- Обновить книгу ---")
        book_id = input("  Введите ID книги для обновления: ")
        book = self.service.find_book_by_id(book_id)
        if not book:
            print(f"Ошибка: Книга с ID {book_id} не найдена.")
            return


        old_title, old_author, old_year = book[0][1], book[0][2], book[0][3]
        print("  Введите новые данные (оставьте пустым, чтобы не менять):")

        title = input(f"  Название ({old_title}): ") or old_title
        author = input(f"  Автор ({old_author}): ") or old_author
        year = input(f"  Год ({old_year}): ") or old_year

        try:
            self.service.update_book(book_id,title, author, year)
            print("Книга успешно обновлена.")
        except Exception as e:
            print(f"Ошибка при обновлении: {e}")

    def _delete_book(self):
        print("\n--- Удалить книгу ---")
        book_id = input("  Введите ID книги для удаления: ")
        try:
            book = self.service.find_book_by_id(book_id)
            if not book:
                print(f"Ошибка: Книга с ID {book_id} не найдена.")
                return
            
            confirm = input(f"  Вы уверены, что хотите удалить '{book[0][1]}'? (y/n): ")
            if confirm.lower() == 'y':
                self.service.delete_book(book_id)
                print("Книга удалена.")
            else:
                print("Удаление отменено.")
        except Exception as e:
            print(f"Ошибка при удалении: {e}")

    def _find_book_by_id(self):
        print("\n--- Найти книгу по ID ---")
        book_id = input("  Введите ID: ")
        book = self.service.find_book_by_id(book_id)
        if book:
            print(f"  Найдено: ID {book[0][0]}: '{book[0][1]}' ({book[0][2]}, {book[0][3]}г.)")
        else:
            print(f"  Книга с ID {book_id} не найдена.")

    def _find_books_by_author(self):
        print("\n--- Найти книги по автору ---")
        author = input("  Введите имя автора (или часть имени): ")
        books = self.service.find_books_by_author(author)
        if not books:
            print(f"  Книги автора '{author}' не найдены.")
        else:
            print(f"  Найдено {len(books)} книг:")
            for book in books:
                print(f"    ID {book[0]}: '{book[1]}' ({book[2]}, {book[3]}г.)")