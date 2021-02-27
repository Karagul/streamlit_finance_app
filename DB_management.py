import sqlite3
from sqlite3 import Error
import json
import os
import time

database = ".\DB\portfolio.db"


# --- DB functions ---

def check_conn():
    if os.path.isfile('.DB\portfolio.db'):
        print("File exist")
    else:
        print("File not exist")

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(database)
    except Error as e:
        print(e)

    return conn

def delete_portfolio(conn):
    """
    Create a new project into the projects table
    :param conn:
    :return: project id
    """
    cur = conn.cursor()
    cur.execute("DROP TABLE portfolio")
    conn.commit()
    print("done")


def create_portfolio(conn):
    """
    Create a new project into the projects table
    :param conn:
    :return: project id
    """
    sql = """ CREATE TABLE IF NOT EXISTS portfolio (
                                        portfolio_ID integer NOT NULL,
                                        stock text NOT NULL,
                                        buyin double NOT NULL,
                                        buyindate date,
                                        amount integer
                                    ); """
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def create_portfolio_entry(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO portfolio(portfolio_ID,stock,buyin, buyindate, amount) 
    VALUES(?,?,?,?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def select_all_playbacks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM portfolio")

    rows = cur.fetchall()
    print("Database: ")
    for row in rows:
        print(row)
    return rows

def get_amount_of_playbacks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    return cur.execute("SELECT SUM * FROM portfolio")


def delete_database(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM portfolio")
    conn.commit()
# --- Main Functions ---

portfolio_array = []
counter = 0
rawportfolio = select_all_playbacks(create_connection())
for x in select_all_playbacks(create_connection()):
    appender = [rawportfolio[counter][1],20.00 , rawportfolio[counter][2], 00.00, rawportfolio[counter][3], 200]
    portfolio_array.append(appender)
    counter = counter +1
    print("X =" ,x, " Counter = ", counter)
print(portfolio_array)


#
#
# conn = create_connection()
# #delete_portfolio(conn)
# create_portfolio(conn)
# print("What do you want to do? DEL / CREATE")
# choice = input()
# if choice == "DEL":
#     delete_database(conn)
# elif choice=="CREATE":
#     playback = (0, 'MSFT', '50.20', '20.02.2020', 1)
#     create_portfolio_entry(conn, playback)
#     playback = (1, 'BMW.DE', '27.75', '30.12.2020', 1)
#     create_portfolio_entry(conn, playback)
#     select_all_playbacks(conn)
# else:
#     select_all_playbacks(conn)

