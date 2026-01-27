from fastapi import FastAPI

from src.currency.router import router

app = FastAPI()


app.include_router(router)