from fastapi import FastAPI

from routers import manage_db, fileProcessing, summary_db, lineage, current_db
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(fileProcessing.router, tags=["File Processing"])
app.include_router(manage_db.router, tags=["Database"])
app.include_router(summary_db.router, tags=["Summary Databse"])
app.include_router(lineage.router,  tags=["Lineage"])
app.include_router(current_db.router, tags=["Current Database"])
