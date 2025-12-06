from domain.listeners.IEventListener import IEventListener

class ManageDBListener(IEventListener):
    def save(self,order_id:int,status:str,details:str,log_time:str,route_info:str,driver_status:str):
            
            sql_query = "INSERT INTO manager_logs (order_id,status,details,log_time) VALUES (%s, %s, %s, %s)"
            data_tuple = (order_id,status,details,log_time)
            self.cursor.execute(sql_query, data_tuple)
            self.connection.commit()
            print(f"[ManagerTable] Менеджер уведомлен... -> запись в таблицу менеджеров.")