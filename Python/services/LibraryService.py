from repositories.interfaces import IBookRepository



class LibraryService:

    def __init__(self, repositories: dict):
        
        self._repositories = repositories

        self._active_repository: IBookRepository = None

    def set_active_repository(self, repo_key: str) -> bool:
    
        repo = self._repositories.get(repo_key)
        
        if repo:
         
            self._active_repository = repo
            
 
            print(f"[Service LOG]: Репозиторий '{repo_key}' активирован.")
            return True
        else:
            print(f"[Service ERROR]: Репозиторий '{repo_key}' не найден.")
            return False

    def _check_active(self):
        if not self._active_repository:
            raise Exception("Ошибка Сервиса: Репозиторий не выбран.")

    def get_all_books(self):
        self._check_active()

        return self._active_repository.get_all()

    def add_book(self, title, author, year):
        self._check_active()
     
        self._active_repository.add(title, author, year)

    def update_book(self, book_id, title, author, year):
        self._check_active()
        self._active_repository.update(book_id, title, author, year)

    def delete_book(self, book_id):
        self._check_active()
        self._active_repository.delete(book_id)

    def find_book_by_id(self, book_id):
        self._check_active()
        return self._active_repository.find_by_id(book_id)

    def find_books_by_author(self, author):
        self._check_active()
        return self._active_repository.find_by_author(author)