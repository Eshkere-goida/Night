from strategies.interfaces.IPaymentProcessor import IPaymentProcessor

class PaymentService:
    def __init__(self, repositories: dict):
        
        self._repositories = repositories

        self._active_repository = 'MySQLTransactionRepository.py'

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
    def process_order(self,amount):
        self._check_active()
        if self._active_repository.pay(amount) == True:
            self._active_repository.add_transaction(amount, method, name,status)
        return 

