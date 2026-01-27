from fastapi import FastAPI

from src.currency.router import router

app = FastAPI()

@app.get("/")
def get_home_page():
    return {
        "status": 200,
        "message": "Hello world!"
    }

app.include_router(router)