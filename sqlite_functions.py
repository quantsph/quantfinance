#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 15:32:59 2017

@author: lampil
"""

import sqlite3
from sqlite3 import Error

## Custom functions

pse_db_path = "/Users/lampil/quantfinance/pse.db"

conn = sqlite3.connect(pse_db_path)
    
query = "SELECT * FROM prices WHERE Symbol = '2GO'"


def select_tablenames(conn):
    '''select names of tables in database'''
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    


def query_df(query,conn):
    '''input SQL query and connections object; output query as a dataframe''' 
    import pandas as pd   
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return pd.DataFrame(rows, columns = [colname[0] for colname in cur.description])




#if __name__ == '__main__':
#    main()