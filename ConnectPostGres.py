
import sys
import Configs
import streamlit as st

import psycopg2
# Connect to PostgreSQL

def fetch_pg_cursor():
    print(Configs.db_name)
    pg_conn = psycopg2.connect(
        database=st.session_state.get('selected_db') or Configs.db_name,
        user=Configs.db_user,
        password=Configs.db_password,
        host=Configs.db_host,  # or your DB host
        port=Configs.db_port
    )
    
    print(pg_conn)

    pg_cursor = pg_conn.cursor()
    # pg_cursor.execute('SELECT * FROM "TD_DEMO_SCHEMA"."FIN_ACCT_TXNS"')
    # rows = pg_cursor.fetchall()
    # print(rows)
    
    return pg_cursor