import csv
from random import choice


# Смешно, правда?


def create_db_and_csv():
    # if not os.path.exists('Assets/Data/results.sqlite3'):
    #     conn = sqlite3.connect('results.sqlite3')
    #     cur = conn.cursor()
    #     cur.execute("""CREATE TABLE IF NOT EXISTS scores(
    #         total_value int)""")
    #     conn.close()
    #
    #     roflil.move('Assets/results.sqlite3', 'Assets/Data/results.sqlite3')
    with open('weapons.csv', 'w', newline='') as csvfile:
        filew = csv.writer(csvfile, delimiter=';',
                           quotechar='"')
        filew.writerow(['Id', 'Name', 'Damage'])
        filew.writerow(['0', 'Hand Sword', '1.0'])
        filew.writerow(['1', 'Sword', '1.5'])
        filew.writerow(['2', 'Cool Sword', '2'])


def select_weapon():
    with open('weapons.csv', 'r') as csvfile:
        filer = csv.reader(csvfile, delimiter=';',
                           quotechar='"')
        num = choice([0, 1, 2])
        for i in filer:
            if i[0] == str(num):
                return i

