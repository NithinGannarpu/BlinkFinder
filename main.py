from fastapi import FastAPI
from routes.items import router as items_router
from routes.blinkit import router as blinkit_router
from routes.firstcry import router as firstcry_router


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Running brudaaa"}

app.include_router(items_router)
app.include_router(blinkit_router)
app.include_router(firstcry_router)