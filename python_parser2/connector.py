import sqlite3
from sqlite3 import Error

from config import DATABASE
from config import DATABASE_WORDS
from sql import sql_create_links_table


def create_connection(db_file):

    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
    return conn


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def create_link(conn, link_data):
    sql = ''' INSERT INTO links(path, domain, protocol)
                VALUES(?,?,?) '''

    c = conn.cursor()
    c.execute(sql, link_data)
    conn.commit()
    return c.lastrowid


def select_all_links(conn,tbl_name):
    c = conn.cursor()
    c.execute(f"SELECT * FROM {tbl_name}")

    rows = c.fetchall()
    
    return rows

def create_word(conn, word_data):
    sql = ''' INSERT INTO words(word, rat, link)
                VALUES(?,?,?) '''

    c = conn.cursor()
    c.execute(sql, word_data)
    conn.commit()
    return c.lastrowid
conn = create_connection(DATABASE)

if conn is not None:
    create_table(conn, sql_create_links_table)
    
