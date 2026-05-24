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

@router.get("/fc/scrape-all")
def scrape_all(pcode: str = DEFAULT_PCODE, db: Session = Depends(get_db)):
    try:
        total_saved = 0

        for page in range(1, 6):
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
                    total_saved += 1

        db.commit()
        return {"message": f"Scrape complete", "snapshots_saved": total_saved}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/fc/saved")
def get_saved_products(pcode: str = DEFAULT_PCODE, db: Session = Depends(get_db)):
    try:
        snapshots = db.query(PriceSnapshot, Product).join(
            Product, PriceSnapshot.pid == Product.pid
        ).filter(
            PriceSnapshot.pcode == pcode
        ).order_by(PriceSnapshot.scraped_at.desc()).all()

        result = []
        for s, p in snapshots:
            result.append({
                "pid": s.pid,
                "name": p.name,
                "brand": p.brand,
                "mrp": s.mrp,
                "disc_price": s.disc_price,
                "discount": s.discount,
                "stock": s.stock,
                "rating": s.rating,
                "shipping": s.shipping,
                "scraped_at": s.scraped_at,
            })

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))