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
        self.create_table()
    
    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS deliveries(
                id INT PRIMARY KEY AUTO_INCREMENT,
                distance FLOAT,
                weight FLOAT,
                cost FLOAT,
                is_express BOOLEAN,
                comment TEXT
            )
        """)
        self.connection.commit()
    
    def save(self, distance,weight,cost,is_express,comment):
        sql_query = "INSERT INTO deliveries (distance,weight,cost,is_express,comment) VALUES (%s, %s, %s, %s, %s)"
        data_tuple = (distance,weight,cost,is_express,comment)
        self.cursor.execute(sql_query, data_tuple)
        self.connection.commit()
        print(f"[DB LOG]: Транзакция сохранена: {distance} км, {weight} кг, {cost} руб")