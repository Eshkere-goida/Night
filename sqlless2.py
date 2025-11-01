import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin",
    database="test"
)
cursor = connection.cursor()

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS books(
#                id INT PRIMARY KEY AUTO_INCREMENT,
#                 title VARCHAR(100),
#                author VARCHAR(100),
#                year INT
#                )
# """)

# cursor.execute("INSERT INTO books(title,author,year) VALUES ('Арап','Мэктэп',2012)")
# cursor.execute("INSERT INTO books(title,author,year) VALUES ('Брарн','Кэвин',1998)")
# cursor.execute("INSERT INTO books(title,author,year) VALUES ('Рррппп','Принтер',1999)")
def get_all():
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    print("Название книги:   Автор:    Год издания:")
    for i in range(len(data)):
        print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
def add_new(title,author,year):
    sql_query = "INSERT INTO books(title,author,year) VALUES (%s,%s,%s)"
    data_tuple = (title,author,year)
    cursor.execute(sql_query,data_tuple)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    print("Название книги:   Автор:    Год издания:")
    for i in range(len(data)):
        print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
def update_existing(title,author,year,id):
    sql_query = "UPDATE books SET title = %s,author = %s,year = %s WHERE id = %s"
    data_tuple = (title,author,year,id)
    cursor.execute(sql_query,data_tuple)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    print("Название книги:   Автор:    Год издания:")
    for i in range(len(data)):
        print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
def del_existing(id):
    sql_query = "DELETE FROM books WHERE id = %s"
    data_tuple = (id,)
    cursor.execute(sql_query,data_tuple)
    cursor.execute("SELECT * FROM books")
    data = cursor.fetchall()
    print("Название книги:   Автор:    Год издания:")
    for i in range(len(data)):
        print(f"{data[i][1]}, {data[i][2]}, {data[i][3]}")
    connection.commit()
def get_specific(id):
    sql_query = "SELECT * FROM books WHERE id = %s"
    data_tuple = (id,)
    cursor.execute(sql_query,data_tuple)
    data = cursor.fetchall()
    print("Название книги:   Автор:    Год издания:")
    print(f"{data[0][1]}, {data[0][2]}, {data[0][3]}")
def get_with_author(author):
    sql_query = "SELECT * FROM books WHERE author = %s"
    data_tuple = (author,)
    cursor.execute(sql_query,data_tuple)
    data = cursor.fetchall()
    print("Название книги:   Автор:    Год издания:")
    print(f"{data[0][1]}, {data[0][2]}, {data[0][3]}")
print("Что вы хотите сделать(введите цифру): \nПоказать все книги \nДобавить одну книгу \nОбновить данные книги(ID) \nУдалить книгу(ID) \nНайти книгу по ID \nНайти книги по автору \n0 если хотите закончить")
while(True):
    ans = int(input())
    if (ans == 1):
        get_all()
    if (ans == 2):
        book_title = input("Введите название книги: ")
        book_author = input("Введите автора: ")
        book_year = int(input("Введите год издания книги: "))
        add_new(book_title,book_author,book_year)
    if (ans == 3):
        book_id = int(input("Введите ID книги: "))
        book_title = input("Введите новое название книги: ")
        book_author = input("Введите нового автора: ")
        book_year = int(input("Введите новый год издания книги: "))
        update_existing(book_title,book_author,book_year,book_id)
    if (ans == 4):
        book_id = int(input("Введите ID книги: "))
        del_existing(book_id)
    if (ans == 5):
        book_id = int(input("Введите ID книги: "))
        get_specific(book_id)
    if (ans == 6):
        book_author = input("Введите автора: ")
        get_with_author(book_author)
    if (ans == 0):
        get_all()
        break


    

connection.close()