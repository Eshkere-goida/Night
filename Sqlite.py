import sqlite3

connection=sqlite3.connect('sqlite3.db')

cursor=connection.cursor()

cursor.execute("""
                CREATE TABLE IF NOT EXISTS channels(
               id INTEGER PRIMARY KEY,
               name TEXT NOT NULL,
               subscribers INTEGER
               )
               """)

cursor.execute("INSERT INTO channels (id,name,subscribers) VALUES (1,'Код и Кофе',150000),(2,'Пиксель-Арт Мастерская',85000),(3,'Музыкальный Уголок',220000)")

connection.commit()

#1

cursor.execute("SELECT * FROM channels")

channels=cursor.fetchall()

for channel in channels:
    channel_name=channel[1]
    channel_subscribers=channel[2]
    print(f"{channel_name}, {channel_subscribers}")

#2

cursor.execute("SELECT name FROM channels WHERE subscribers > 100000")

channels=cursor.fetchall()

for channel in channels:
    channel_name=channel[0]
    
    print(channel_name)


#3
cursor.execute("SELECT COUNT(name) FROM channels")

channels=cursor.fetchall()

print(channels[0][0])


#4
cursor.execute("UPDATE channels SET subscribers = 160000 WHERE id = 1")
connection.commit()


#5
cursor.execute("SELECT * FROM channels WHERE id = 2")

channels=cursor.fetchall()

for channel in channels:
    channel_id = channel[0]
    channel_name=channel[1]
    channel_subscribers=channel[2]
    print(f"ID: {channel_id}, Название: {channel_name}, Подписчики: {channel_subscribers}")
    

cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos(
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               views INTEGER,
               channel_id INTEGER,
               FOREIGN KEY(channel_id) REFERENCES channels(id)
               )
               """)

cursor.execute("INSERT INTO videos (id,title,views,channel_id) VALUES (1,'Python для начинающих. Урок 1',55000,1),(2,'Как нарисовать дерево(Pixel Art)',12000,2),(3,'Топ 5 гитарных риффов',300000,3),(4,'SQLite и Python (Продвинутый)',25000,1),(5,'Обзор нового синтезатора',110000,3)")
connection.commit()

#6
cursor.execute("SELECT videos.title,channels.name FROM videos JOIN channels ON videos.channel_id=channels.id")
channels = cursor.fetchall()

for i in range(len(channels)):
    print(f"Название канала: {channels[i][1]}, Видео: {channels[i][0]}")


#7
cursor.execute("SELECT videos.title,channels.name FROM videos JOIN channels ON videos.channel_id=channels.id WHERE channels.name = 'Код и Кофе'")
channels = cursor.fetchall()
for i in range(len(channels)):
    print(f"Название канала: {channels[i][1]}, Видео: {channels[i][0]}")

#8
cursor.execute("SELECT COUNT(videos.id),channels.name FROM videos JOIN channels ON videos.channel_id=channels.id GROUP BY channels.name")

for i in range(len(channels)):
    print(f"Название канала: {channels[i][1]}, Кол-во видео: {channels[i][0]}")

#9
cursor.execute("SELECT videos.title FROM videos WHERE videos.views > 100000")
channels = cursor.fetchall()
for i in range(len(channels)):
    print(channels[i][0])


#10
cursor.execute("SELECT SUM(videos.views) FROM videos JOIN channels ON videos.channel_id=channels.id GROUP BY channels.name HAVING videos.channel_id =3")
channels = cursor.fetchall()
print(channels[0][0])

connection.close()

