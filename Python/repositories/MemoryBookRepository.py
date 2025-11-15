from .interfaces.IBookRepository import IBookRepository


class MemoryBookRepository(IBookRepository):
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
            if self.books[i]['id'] == book_id:
                deleted_title = self.books[i]['title']
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