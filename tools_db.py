import sqlite3
from sqlite3 import Error
from pathlib import Path

BASE_DIR = Path(__file__).parent


def create_connection(path):
   """
   Устанавливает соединение с БД
   :param path: полный путь к файлу БД
   :return: объект connection - через этот объект выполняются SQL-запросы
   """
   try:
       print("Connection to SQLite DB successful")
       return sqlite3.connect(path)
   except Error as e:
       print(f"The error '{e}' occurred")


def execute_query(connection, query):
   """
   Выполняет SQL-запросы к БД
   :param connection: объект connection
   :param query: SQL-запрос
   """
   cursor = connection.cursor()  # создаем объект cursor, он позволяет делать SQL-запросы к базе
   try:
       cursor.execute(query)
       connection.commit()
       print("Query executed successfully")
   except Error as e:
       print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
   """
   Выполняет SQL-запросы к БД и возвращает результат
   :param connection: объект connection
   :param query: SQL-запрос
   :return: результат SQL-запроса
   """
   cursor = connection.cursor()
   try:
       cursor.execute(query)
       result = cursor.fetchall()
       return result
   except Error as e:
       print(f"The error '{e}' occurred")


create_quote_table = """
CREATE TABLE IF NOT EXISTS quotes (
id INTEGER PRIMARY KEY AUTOINCREMENT,
author TEXT NOT NULL,
text TEXT NOT NULL
);
"""

create_quotes = """
INSERT INTO
quotes (author,text)
VALUES
('Rick Cook', 'Программирование сегодня — это гонка разработчиков программ...'),
('Waldi Ravens', 'Программирование на С похоже на быстрые танцы на только...');
"""


if __name__ == "__main__":
    connection = create_connection(BASE_DIR / 'db.sqlite')

