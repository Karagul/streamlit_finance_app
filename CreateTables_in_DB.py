import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = r".\DB\portfolio.db"

    sql_drop_playback = """DROP TABLE portfolio"""

    sql_create_playback_table = """ CREATE TABLE IF NOT EXISTS portfolio (
                                        portfolio_ID integer NOT NULL,
                                        stock text NOT NULL,
                                        buyin double NOT NULL,
                                        buyindate date
                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        #drop table
        create_table(conn, sql_drop_playback)

        # create playbacks table
        create_table(conn, sql_create_playback_table)

    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
