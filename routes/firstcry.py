from fastapi import APIRouter, HTTPException
from services.fcrequester import fetch_products,parse_products
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PCODE = os.getenv("FC_DEFAULT_PCODE")

router = APIRouter()

@router.get("/fc")
def firstcry(page: int = 1,pcode: str = "xxxx"):
    try:
        raw = fetch_products(page=page,pcode=DEFAULT_PCODE)
        print(raw)
        products = parse_products(raw)
        return {"data": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))