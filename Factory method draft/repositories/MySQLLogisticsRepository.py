import mysql.connector

class MySQLLogisticsRepository:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        self.cursor = self.connection.cursor()
        self.create_tables()
    
    def create_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries(
                id INT PRIMARY KEY AUTO_INCREMENT,
                transport_type VARCHAR(100),
                from_city TEXT,
                to_city TEXT,
                distance FLOAT,
                weight FLOAT,
                cost FLOAT,
                is_express BOOLEAN,
                comment TEXT
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS manager_logs(
                id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT,
                status TEXT,
                details TEXT,
                log_time DATE
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS driver_tasks(
                id INT PRIMARY KEY AUTO_INCREMENT,
                order_id INT,
                route_info TEXT,
                driver_status VARCHAR(100)
            )
        """)

        self.connection.commit()
    
    def save_order(self, transport_type,from_city,to_city,distance,weight,cost,is_express,comment):
        sql_query = "INSERT INTO deliveries (transport_type,from_city,to_city,distance,weight,cost,is_express,comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        data_tuple = (transport_type,from_city,to_city,distance,weight,cost,is_express,comment)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"[MainTable] Заказ сохранен в 'deliveries'")
    def save_manager_log(self,order_id,status,details):
        sql_query = "INSERT INTO manager_logs (order_id,status,details,log_time) VALUES (%s, %s, %s, NOW())"
        data_tuple = (order_id,status,details)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"[ManagerTable] Менеджер уведомлен... -> запись в таблицу менеджеров.")
    def save_driver_task(self,order_id,route_info,driver_status):
        sql_query = "INSERT INTO driver_tasks (order_id,route_info,driver_status) VALUES (%s, %s, %s)"
        data_tuple = (order_id,route_info,driver_status)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"[DriverTable] Водитель получил задачу... -> запись в таблицу водителей.")
        