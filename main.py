from fastapi import FastAPI
from routes.items import router as items_router
from routes.blinkit import router as blinkit_router


app = FastAPI()

app.get("/")
def root():
    return {"message": "Running brudaaa"}

