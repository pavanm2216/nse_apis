from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class UTRUpdate(Base):
    __tablename__ = "utr_updates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(10), index=True)
    bank_name = Column(String(100))
    account_no = Column(String(20))
    ifsc = Column(String(11))
    utr_no = Column(String(30))
    transfer_date = Column(String(12))
    order_id = Column(String(12))
    status = Column(String(5))
    message = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
