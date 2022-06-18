'''парсер работает частично.  В данных есть моменты, где деления столбцов
через "," не работает. Выбранный делитель запятая плохой для обработки
текстовых данных с названиями и речью Я еще поработаю над ним'''

import csv
import sqlite3
from os import path

FILE_DIR = path.dirname(path.abspath(__file__))
DATA_BASE = path.join(FILE_DIR, 'db.sqlite3')
FILE = ('category', 'genre', 'titles', 'review', 'genre_title', 'comments')

path_bd = {}
for path_file in FILE:
    path_bd[f'reviews_{path_file}'] = path.join(FILE_DIR, 'static', 'data',
                                                f'{path_file}.csv')

path_bd['users_user'] = path.join(FILE_DIR, 'static', 'data', 'users.csv')

con = sqlite3.connect(DATA_BASE)
cur = con.cursor()

for name, path_file in path_bd.items():
    data_file = open(path_file, 'r', encoding='utf-8')
    rows = csv.reader(data_file, delimiter=',')
    items = rows.__next__()
    print(items)
    count = ','.join('?' * len(items))
    print(count)
    cur.executemany(f'INSERT INTO {name} VALUES ({count})', rows)
    cur.execute(f'SELECT * FROM {name}')
    print(cur.fetchall())

con.commit()
con.close()
