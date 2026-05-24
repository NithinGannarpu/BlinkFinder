from sqlalchemy import Column, String, Integer, Numeric, TIMESTAMP, ForeignKey, Text
from sqlalchemy.sql import func
from database import Base

class Product(Base):
    __tablename__ = "products"

    pid   = Column(String(20), primary_key=True)
    name  = Column(Text)
    brand = Column(String(100))
    size  = Column(String(100))


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    pid        = Column(String(20), ForeignKey("products.pid"), nullable=False)
    mrp        = Column(Integer)
    disc_price = Column(Numeric(10, 2))
    discount   = Column(Integer)
    stock      = Column(Integer)
    rating     = Column(Numeric(3, 2))
    shipping   = Column(String(100))
    pcode      = Column(String(10))
    scraped_at = Column(TIMESTAMP, server_default=func.now())