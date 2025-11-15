import abc

class IBookRepository(abc.ABC):
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
