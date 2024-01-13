import sqlite3, csv, os
from random import choice
# Смешно, правда?
import shutil as roflil


def create_db_and_csv():
    if not os.path.exists('Assets/Data/results.sqlite3'):
        conn = sqlite3.connect('results.sqlite3')
        cur = conn.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS scores(
            total_value int)""")
        conn.close()

        roflil.move('results.sqlite3', 'Assets/Data/results.sqlite3')
    if not os.path.exists('Data/weapons.csv'):
        with open('weapons.csv', 'w', newline='') as csvfile:
            filew = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            filew.writerow(['Id', 'Name', 'Damage'])
            filew.writerow(['0', 'Hand_Sword', '1.0'])
            filew.writerow(['1', 'Sword', '1.5'])
            filew.writerow(['2', 'Coolest_Sword', '2.0'])

        roflil.move('weapons.csv', 'Assets/Data/weapons.csv')


def get_best_value():
    conn = sqlite3.connect('results.sqlite3')
    cur = conn.cursor()
    res = cur.execute("""SELECT MAX(total_value) FROM scores""").fetchone()
    conn.close()
    return res[0]


def insert_value(score):
    conn = sqlite3.connect('results.sqlite3')
    cur = conn.cursor()
    cur.execute(f"""INSERT INTO scores(total_value) VALUES({score})""")
    conn.close()


def select_weapon():
    with open('Assets/Data/weapons.csv', 'r') as csvfile:
        filer = csv.reader(csvfile, delimiter=';',
                           quotechar='"')
        num = choice([0, 1, 2])
        for i in filer:
            if i[0] == str(num):
                return i
