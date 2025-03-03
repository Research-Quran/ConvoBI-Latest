import streamlit as st
from llm import ollama_use
from SQLUtility import execute
import lineagequeries
import Configs
import requests

import streamlit as st
import streamlit_authenticator as stauth
import yaml 
from streamlit_option_menu import option_menu
from pathlib import Path
from navigation import make_sidebar
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import ConnectPostGres
import ConnectNeo4j
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
import urllib.parse



def process_file(file_option):
    if st.session_state['file_uploader'] is not None:
        print(st.session_state['file_uploader'])
        print('inside process_file')
        print('Uploaded file ' + st.session_state['file_uploader'].name)
        excel_file=pd.ExcelFile(st.session_state['file_uploader'])
        
        db_user = Configs.db_user
        db_password = urllib.parse.quote_plus(Configs.db_password)  # URL-encode the password
        db_host =Configs.db_host
        db_port = Configs.db_port
        db_name = st.session_state.get('selected_db') or Configs.db_name
        engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
        session = Session(engine)
        for sheet in excel_file.sheet_names:
            table_name = sheet
            print(f"Processing sheet: {sheet}")
            data = pd.read_excel(st.session_state['file_uploader'], sheet_name=sheet)
            #print(data.columns)
            print(f"Inserting data into table: {table_name}")
            try:
                print(engine)
                data.to_sql(table_name, engine, schema="genaipoc", if_exists=file_option.lower(), index=False)
                print(f"Data from sheet '{sheet}' successfully inserted into table '{table_name}'")
                st.success("Imported "+sheet +" successfully. into "+db_name)
              
            except Exception as e:
                print(f"Error inserting data from sheet '{sheet}' into table '{table_name}': {str(e)}")
                st.error("Importing "+sheet +" failed."+ str(e))
        
        try:
            
            #cursor=ConnectPostGres.fetch_pg_cursor()
            if(file_option.upper()=='REPLACE'):
                session.execute(text(open('files/DB_Workflow_replace.sql','r').read()))
            #cursor.connection.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            session.execute(text(open('files/DB_Workflow.sql','r').read()))
            st.success("Transformed Data uploaded to Target tables.")
            session.commit()
            session.close()  
            
        except Exception as e:
            session.rollback()
            session.close()  
            
            print('Exception in executing the DB workflow. Error '+ str(e))
            st.error('Error in DB workflow'+ str(e))
        
        try:
            ConnectNeo4j.fetch_data_from_neo4j()
            st.success("Graph Database Generated Successfully.")
        except Exception as ex:
            print('Exception in Generating Graph DB.'+str(ex))
            st.error('Error generating Graph DB.'+str(ex))
            
    
    
def main():
    
    make_sidebar()
    st.markdown("Current Database: "+st.session_state.get('selected_db',Configs.db_name))
    #st.error("Importing the file Replaces the existing data")
    
    # with st.form(key='my_form'):
    #     text_input = st.text_input(label='Enter Database name')
    #     submit_button = st.form_submit_button(label='Submit')
    #     if submit_button:
    #         st.write(f'hello {text_input}')
    #         SQLUtility.execute('create database '+text_input)
    #         st.session_state.selected_db=text_input
 
 
    with open("files/Metadata_Template.xlsx", "rb") as file:
                btn = st.download_button(
            label="Download Template for Metadata",
            data=file,
            file_name="Metadata_Template.xlsx",
            mime="application/xlsx",
        )
                file_option = st.radio(
    "Action on File Import",
    ["Append", "Replace"],
    index=1,
)
                file_uploaded=st.file_uploader('Import Metadata file', type=['xlsx'],
                                       accept_multiple_files=False, key="file_uploader", help=None, 
                                    on_change=process_file, args=(file_option,), kwargs=None,  
                                    disabled=False, label_visibility="visible")
        
if __name__ == "__main__":
    main()