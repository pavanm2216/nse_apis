from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class SIPAmcPause(Base):
    __tablename__ = "sip_amc_pauses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(15), index=True)
    reg_type = Column(String(5))
    sip_reg_no = Column(String(15), index=True)
    modification_type = Column(String(10))
    no_of_installments = Column(String(5))
    pause_from = Column(String(10))
    filler_1 = Column(String(50))
    filler_2 = Column(String(50))
    filler_3 = Column(String(50))
    filler_4 = Column(String(50))
    nse_remarks = Column(String(1000))
    status_flag = Column(String(1))
    request_id = Column(String(10))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
