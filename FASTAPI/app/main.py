from fastapi import FastAPI
from routers import manage_db, fileProcessing, summary_db


app = FastAPI()
app.include_router(fileProcessing.router, prefix="/file", tags=["File Processing"])
app.include_router(manage_db.router, prefix="/db", tags=["Database"])
app.include_router(summary_db.router, prefix="/summary_db", tags=["Summary Databse"])
