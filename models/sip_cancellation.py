from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class SIPCancellation(Base):
    __tablename__ = "sip_cancellations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(10), index=True)
    sip_reg_no = Column(String(15))
    remarks = Column(String(100))
    can_status = Column(String(15))
    can_remark = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
