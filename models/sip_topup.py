from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class SIPTopupRegistration(Base):
    __tablename__ = "sip_topup_registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(10), index=True)
    req_type = Column(String(4))
    sip_reg_no = Column(String(15))
    installment_amount = Column(String(20))
    topup_frequency = Column(String(20))
    topup_amount = Column(String(20))
    start_date = Column(String(10))
    end_date = Column(String(10))
    internal_ref_no = Column(String(25))
    primary_holder_mobile = Column(String(10))
    primary_holder_email = Column(String(50))
    reg_id = Column(String(15))
    reg_status = Column(String(15))
    reg_remark = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
