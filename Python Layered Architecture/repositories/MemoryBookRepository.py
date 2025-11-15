from .interfaces.IBookRepository import IBookRepository

class MemoryBookRepository(IBookRepository):
    def __init__(self):
        self.books = []
        self.next_id = 1

    def get_all(self):
        result = []
        for book in self.books:
            result.append([book['id'], book['title'], book['author'], book['year']])
        print("ID | Название книги | Автор | Год издания:")
        for book in result:
            print(f"  {book[0]} | {book[1]} | {book[2]} | {book[3]}")
        return result

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
            if book['id'] == int(book_id): 
                book['title'] = title
                book['author'] = author
                book['year'] = year
                return True
        return False

    def delete(self, book_id):
        for i in range(len(self.books)):
            if self.books[i]['id'] == int(book_id): 
                del self.books[i]
                return True
        
        return False

    def find_by_id(self, book_id):
        for book in self.books:
            if book['id'] == int(book_id):  
                result = [[book['id'], book['title'], book['author'], book['year']]]
                return result
        return None

    def find_by_author(self, author_name):
        found_books = []
        for book in self.books:
            if author_name.lower() in book['author'].lower():
                found_books.append([book['id'], book['title'], book['author'], book['year']])
        return found_books