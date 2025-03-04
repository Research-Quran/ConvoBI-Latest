import psycopg2
import Configs
import SQLUtility
 
# Establishing the connection
def schema_td():
    
    # Query to fetch schema information
    schema_info = SQLUtility.execute("""
        SELECT table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema = 'TD_DEMO_SCHEMA'
        ORDER BY table_name, ordinal_position;
    """)
    
    # Fetching the results
    
    
    # Displaying the schema information
    #print(schema_info)
    # for table, column, data_type in schema_info:
    #     print(f"Table: {table}, Column: {column}, Data Type: {data_type}")
    
    # Closing the cursor and connection
    return str(schema_info)

schema_td()