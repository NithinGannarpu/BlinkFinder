from fastapi import APIRouter
from services.scraper import search_blinkit

router = APIRouter()

@router.get("/blinkit/{product}")
def blinkit(product: str):
    return search_blinkit(product)