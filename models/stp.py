from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class STPRegistration(Base):
    __tablename__ = "stp_registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_code = Column(String(10), index=True)
    from_scheme_code = Column(String(20))
    to_scheme_code = Column(String(20))
    buy_sell_type = Column(String(10))
    transaction_mode = Column(String(1))
    folio_no = Column(String(15))
    internal_ref_number = Column(String(25))
    start_date = Column(String(10))
    frequency_type = Column(String(20))
    no_of_transfers = Column(String(10))
    to_date = Column(String(10))
    installment_amount = Column(String(20))
    installment_units = Column(String(20))
    first_order_today = Column(String(1))
    sub_broker_code = Column(String(15))
    euin_declaration = Column(String(1))
    euin_number = Column(String(7))
    remarks = Column(String(200))
    sub_broker_arn_code = Column(String(20))
    mobile = Column(String(10))
    email = Column(String(50))
    reg_id = Column(String(15))
    reg_status = Column(String(15))
    reg_remark = Column(Text)
    member_unique_id = Column(String(25))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
