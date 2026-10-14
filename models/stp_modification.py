from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class STPModification(Base):
    __tablename__ = "stp_modifications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sys_reg_no = Column(String(15), index=True)
    primary_holder_email = Column(String(50))
    primary_holder_mobile = Column(String(10))
    sub_broker_code = Column(String(15))
    sub_broker_arn = Column(String(20))
    euin_number = Column(String(7))
    folio_no = Column(String(15))
    trans_mode = Column(String(20))
    amount = Column(String(20))
    remarks = Column(String(100))
    send_2fa = Column(String(1))
    send_comm = Column(String(1))
    filler_1 = Column(String(20))
    filler_2 = Column(String(20))
    member_unique_id = Column(String(25))
    status = Column(String(50))
    status_remarks = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
