from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class MandateRegistration(Base):
    __tablename__ = "mandate_registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(10), index=True)
    amount = Column(String(20))
    mandate_type = Column(String(1))
    account_no = Column(String(40))
    ac_type = Column(String(2))
    ifsc_code = Column(String(11))
    micr_no = Column(String(9))
    start_date = Column(String(10))
    end_date = Column(String(10))
    registration_date = Column(String(10))
    member_mandate_no = Column(String(20))
    reg_id = Column(String(15))
    reg_status = Column(String(15))
    reg_remark = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
