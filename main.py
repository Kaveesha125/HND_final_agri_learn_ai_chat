from fastapi import FastAPI
from routers import chat

app = FastAPI()

app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"status": "site is up and running"}
