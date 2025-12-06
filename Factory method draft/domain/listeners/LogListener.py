from domain.listeners.IEventListener import IEventListener

class LogListener(IEventListener):
    def save(self,order_id:int,status:str,details:str,log_time:str,route_info:str,driver_status:str):
            sql_query = "INSERT INTO driver_tasks (order_id,route_info,driver_status) VALUES (%s, %s, %s)"
            data_tuple = (order_id,route_info,driver_status)
            self.cursor.execute(sql_query, data_tuple)
            self.connection.commit()
            print(f"[DriverTable] Водитель получил задачу... -> запись в таблицу водителей.")