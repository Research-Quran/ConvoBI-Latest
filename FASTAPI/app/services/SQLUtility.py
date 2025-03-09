import psycopg2
import pandas as pd
from langchain_community.utilities.sql_database import SQLDatabase
from backend import Configs

from services import ConnectPostGres
import sqlalchemy
from sqlalchemy import DECIMAL
import os

# DATABASE_FILE = os.path.join(os.path.dirname(__file__), "selected_database.txt")
DATABASE_FILE = "selected_database.txt"
# Function to read the selected database from the file
def get_selected_database():
    try:
        with open(DATABASE_FILE, "r") as file:
            db_name = file.read().strip()
            if db_name:
                return db_name
    except FileNotFoundError:
        pass
    return Configs.db_name  # Fallback to Configs.db_name if file is missing or empty


def execute(sql_query):

    try:
       
        cur = ConnectPostGres.fetch_pg_cursor()
        cur.execute('''{}'''.format(sql_query))
        rows = cur.fetchall()
        columns = [description[0] for description in cur.description]
        df=pd.DataFrame(rows, columns=columns)  
        #print(columns)
        print(df.head())
        cur.close()
    
        return df

    except Exception as e:
        print(e)

#execution('SELECT * FROM "TD_DEMO_SCHEMA"."SRC1_FILE"')

def execute(query,parameters=''):
    db_user = Configs.db_user
    db_password =Configs.db_password
    db_host =Configs.db_host
    db_port = Configs.db_port
    db_name = get_selected_database()
    db = SQLDatabase.from_uri(f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}",schema='TD_DEMO_SCHEMA')
    
# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}",sample_rows_in_table_info=1,include_tables=['customers','orders'],custom_table_info={'customers':"customer"})


    response=db.run(query,parameters=parameters,include_columns='true')
    #df=pd.DataFrame(eval(response))
    if(len(response)==0):
        response=None
    return (response)
