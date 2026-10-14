from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class DailyXSIPCancellation(Base):
    __tablename__ = "daily_xsip_cancellations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(10), index=True)
    xsip_reg_no = Column(String(15))
    xsip_cancel_date = Column(String(10))
    remarks = Column(String(100))
    can_status = Column(String(15))
    can_remark = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
