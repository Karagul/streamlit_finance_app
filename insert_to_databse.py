import sqlite3
from sqlite3 import Error

#Script to handle all datebase input queries
#Pos. Name for Module: insert.py
#Pos. Method Call for Module: sqdb.insert(db,table,lol[]) // List[] or LOL[] as entry currently undefined

#Idea: Save fav. Database in some package store // Global Var or config.txt (pref)

#Known Issue:
# - Administration of Server Access Rights
# - Error Handling of invalid (identity error) input

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def create_portfolio_entry(conn, project):
    """
    Create a new project into the projects table
    :param conn:
    :param project:
    :return: project id
    """
    sql = '''INSERT INTO portfolio(portfolio_ID,stock,buyin, buyindate) 
    VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid


def main():
    database = r".\DB\portfolio.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # create new playback dataset
        playback = (0, 'MSFT', '50,20', '20.02.2020');
        project_id = create_portfolio_entry(conn, playback)


if __name__ == '__main__':
    main()

def insertplayback(track,location):
    database = r".\DB\portfolio.db"

    #develop array of inputs


    # create a database connection
    conn = create_connection(database)
    with conn:
        # create new playback dataset
        playback = (0, 'TRACK_ID', 'TRACK_NAME', 'ARTIST_ID', 'ARTIST_NAME', 'GENRE_ID', 'GENRE_NAME', 128, 'LOCATION', 1, 90);
        playback_id = create_playback(conn, playback)

