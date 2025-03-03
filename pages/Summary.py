import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st
import navigation
import Configs
import SQLUtility

def main():
    navigation.make_sidebar()
    st.markdown("Current Database: " + st.session_state.get('selected_db', Configs.db_name))
    
    rows = SQLUtility.execute(""" 
        SELECT  
            c.table_schema AS schema,
            c.table_name AS table,
            COUNT(c.column_name) AS "No Of Columns",
            pg_size_pretty(pg_total_relation_size(t.oid)) AS size
        FROM 
            information_schema.columns c
        JOIN 
            pg_class t ON c.table_name = t.relname
        JOIN 
            pg_namespace n ON n.oid = t.relnamespace 
                AND c.table_schema = n.nspname
        WHERE 
            c.table_schema NOT IN ('pg_catalog', 'information_schema')
            AND c.table_schema = 'genaipoc'
        GROUP BY 
            c.table_schema,
            c.table_name,
            t.oid
        ORDER BY 
            c.table_schema,
            c.table_name;
    """)
    
    if rows is not None:
        # Debug print to see what we're getting
        print("Type of rows:", type(rows))
        print("Content of rows:", rows)
        
        try:
            # Convert the data into the correct format
            if isinstance(rows, str):
                import ast
                rows = ast.literal_eval(rows)
            
            # Create DataFrame
            df = pd.DataFrame(rows)
            
            # Rename columns to match desired format
            df = df.rename(columns={
                'schema': 'Schema',
                'table': 'Table',
                'No Of Columns': 'No Of Columns',
                'size': 'Size'
            })
            
            # Ensure column order
            df = df[['Schema', 'Table', 'No Of Columns', 'Size']]
            
            print("DataFrame created successfully:")
            print(df)
            st.table(df)
            
        except Exception as e:
            st.error(f"Error creating DataFrame: {str(e)}")
            print(f"Error details: {str(e)}")
            
            # Additional debug information
            if 'rows' in locals():
                print("Rows data structure:")
                print(f"Type: {type(rows)}")
                if isinstance(rows, list) and len(rows) > 0:
                    print(f"First row type: {type(rows[0])}")
                    print(f"First row content: {rows[0]}")
    else:
        st.error("No data returned from the query")

if __name__ == '__main__':
    main()