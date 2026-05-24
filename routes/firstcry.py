from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from services.fcrequester import fetch_products, parse_products
from models.item import Product, PriceSnapshot
from database import get_db
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

DEFAULT_PCODE = os.getenv("FC_DEFAULT_PCODE")

router = APIRouter()

@router.get("/fc")
def firstcry(page: int = 1, pcode: str = DEFAULT_PCODE, db: Session = Depends(get_db)):
    # try:
        raw = fetch_products(page=page, pcode=pcode)
        products = parse_products(raw)

        for p in products:
            existing = db.query(Product).filter(Product.pid == p["PId"]).first()
            if not existing:
                db.add(Product(
                    pid=p["PId"],
                    name=p["PNm"],
                    brand=p["BNm"],
                    size=p["size"],
                ))

            today = date.today()
            snapshot_exists = db.query(PriceSnapshot).filter(
                PriceSnapshot.pid == p["PId"],
                PriceSnapshot.pcode == pcode,
                PriceSnapshot.scraped_at >= datetime(today.year, today.month, today.day)
            ).first()

            if not snapshot_exists:
                db.add(PriceSnapshot(
                    pid=p["PId"],
                    mrp=p["MRP"],
                    disc_price=p["discprice"],
                    discount=p["Disc"],
                    stock=p["CrntStock"],
                    rating=p["rating"],
                    shipping=p["shippingdate"],
                    pcode=pcode,
                ))

        db.commit()
        return {"data": products}

    # except Exception as e:
    #     db.rollback()
    #     raise HTTPException(status_code=500, detail=str(e))