from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access the variables
llm_URL = os.getenv("llm_URL")
llm_model = os.getenv("llm_model")

db_host = os.getenv("db_host")
db_port = os.getenv("db_port")
db_name = os.getenv("db_name")
db_user = os.getenv("db_user")
db_password = os.getenv("db_password")


DATABASE_URL = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

graph_url = os.getenv("Graph_URL")

Neo4JS_DB_Url = os.getenv("Neo4JS_DB_Url")
NEO4JS_DB_User = os.getenv("NEO4JS_DB_User")
NEO4JS_DB_Password = os.getenv("NEO4JS_DB_Password")
NEO4JS_DB_Name = os.getenv("NEO4JS_DB_Name")

# Print to verify (remove in production)
print("LLM URL:", llm_URL)
print("Database Host:", db_host)
print("Neo4j URL:", Neo4JS_DB_Url)
