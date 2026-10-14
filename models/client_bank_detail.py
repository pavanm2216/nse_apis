from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.sql import func
from database import Base


class ClientBankDetail(Base):
    __tablename__ = "client_bank_details"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(20), index=True)
    action_type = Column(String(2))
    account_type = Column(String(2))
    account_no = Column(String(40))
    micr_no = Column(String(9))
    ifsc_code = Column(String(11))
    default_bank_flag = Column(String(1))
    status = Column(String(20))
    error_remark = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
