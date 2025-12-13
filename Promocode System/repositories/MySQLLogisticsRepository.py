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
                transport_type VARCHAR(50),
                from_city TEXT,
                to_city TEXT,
                distance FLOAT,
                weight FLOAT,
                original_cost FLOAT,  
                final_cost FLOAT,     
                discount_amount FLOAT DEFAULT 0,  
                promo_code VARCHAR(50),  
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
                log_time DATETIME
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
       
    
    def save_order(self, transport_type, from_city, to_city, distance, weight, original_cost, final_cost, discount_amount, promo_code, is_express, comment):
        try:
            sql_query = """INSERT INTO deliveries (transport_type, from_city, to_city, distance, weight, original_cost, final_cost, discount_amount, promo_code, is_express, comment) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            data_tuple = (transport_type, from_city, to_city, distance, weight, original_cost, final_cost, discount_amount, promo_code, is_express, comment)
            self.cursor.execute(sql_query, data_tuple)
            self.connection.commit()
            order_id = self.cursor.lastrowid
            print(f"[MainTable] Заказ сохранен в 'deliveries' (ID: {order_id})")
            return order_id
            
        except mysql.connector.Error as err:
            print(f"Ошибка при сохранении заказа: {err}")
            self.create_tables()
            return self.save_order(transport_type, from_city, to_city, distance, weight, original_cost, final_cost, discount_amount, promo_code, is_express, comment)
        
    def save_driver_task(self, order_id, route_info, driver_status="НОВЫЙ"):
        sql_query = "INSERT INTO driver_tasks (order_id, route_info, driver_status) VALUES (%s, %s, %s)"
        data_tuple = (order_id, route_info, driver_status)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"[DriverTable] Водитель получил задачу... -> запись в таблицу водителей.")
    
    
    def save_manager_log(self, order_id, status, details):
        sql_query = "INSERT INTO manager_logs (order_id, status, details, log_time) VALUES (%s, %s, %s, NOW())"
        data_tuple = (order_id, status, details)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"[ManagerTable] Менеджер уведомлен... -> запись в таблицу менеджеров.")