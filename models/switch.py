from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class SwitchTransaction(Base):
    __tablename__ = "switch_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_ref_number = Column(String(19))
    from_scheme_code = Column(String(20))
    to_scheme_code = Column(String(20))
    buy_sell_type = Column(String(10))
    client_code = Column(String(10), index=True)
    demat_physical = Column(String(1))
    amount = Column(String(20))
    units = Column(String(20))
    all_units = Column(String(1))
    folio_no = Column(String(15))
    remarks = Column(String(200))
    kyc_flag = Column(String(1))
    sub_broker_code = Column(String(15))
    euin_number = Column(String(20))
    euin_declaration = Column(String(1))
    sub_broker_arn = Column(String(20))
    mobile_no = Column(String(10))
    email = Column(String(50))
    filler1 = Column(String(50))
    filler2 = Column(String(50))
    filler3 = Column(String(50))
    trxn_so_order_id = Column(String(12))
    trxn_si_order_id = Column(String(12))
    trxn_status = Column(String(15))
    trxn_remark = Column(Text)
    member_unique_id = Column(String(25))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
