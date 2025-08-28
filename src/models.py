from sqlalchemy import Column, Integer, String, Float, Date, BigInteger
from database import Base


class StockPrice(Base):
    __tablename__ = "trading_data"

    id = Column(Integer, primary_key=True, index=True)
    trading_symbol = Column(String(50), nullable=False, index=True)
    date = Column(Date, nullable=False)
    open = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    close = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)
