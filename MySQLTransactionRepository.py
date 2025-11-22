
import mysql.connector

class MySQLTransactionRepository:
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
            CREATE TABLE IF NOT EXISTS transactions(
                id INT PRIMARY KEY AUTO_INCREMENT,
                amount INT,
                payment_method VARCHAR(100),
                status VARCHAR(100),
                created_at DATE
            )
        """)
        self.connection.commit()
    def add_transaction(self,amount,method_name,status):
        sql_query = "INSERT INTO transactions (amount,method_name,status,date) VALUES (%s,%s,%s,CURDATE())"
        data_tuple = (amount,method_name,status)
        self.cursor.execute(sql_query,data_tuple)
        self.connection.commit()
    