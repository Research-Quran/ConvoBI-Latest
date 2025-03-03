import ConnectPostGres
import streamlit as st
from navigation import make_sidebar
import Configs
from st_table_select_cell import st_table_select_cell
import SQLUtility

def list_all_databases():
    # cur=ConnectPostGres.connect_pg()
    df=SQLUtility.execute('SELECT datname FROM pg_database')
    # rows = cur.fetchall()
    
    return eval(df)

def set_database(db_name):
    print('Select DB :'+db_name)
    st.session_state.selected_db=db_name
    print(st.session_state)
    st.success(db_name+' Selected.') 
    
    

def main():
    make_sidebar()
    st.markdown("Current Database: "+st.session_state.get('selected_db',Configs.db_name))
    st.write("List of all databases")
    db_list=list_all_databases()
    
    cols=st.columns((1,2,3))
    fields=["Sl No","Table","Action"]
    
    for col,fieldname in zip(cols , fields):
        col.write(fieldname)
        
    i=0
    for value in enumerate(db_list):
        db_name=value[1]['datname']
        i=i+1
        col1, col2, col3 = st.columns((1, 2, 3))
        col1.write(i)  # index
        col2.write(db_name)  # Database name
        button_type = "Select" 
        button_phold = col3.empty()  # create a placeholder
        do_action = button_phold.button(button_type, key=i)
        if do_action:
            set_database(db_name)

    
    
if __name__ == "__main__":
    main()