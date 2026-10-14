from sqlalchemy import Column, String, Integer, Numeric, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class OrderTransaction(Base):
    __tablename__ = "order_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_ref_number = Column(String(19))
    scheme_code = Column(String(20))
    trxn_type = Column(String(1))
    buy_sell_type = Column(String(10))
    client_code = Column(String(10), index=True)
    demat_physical = Column(String(1))
    order_amount = Column(String(20))
    folio_no = Column(String(15))
    remarks = Column(String(200))
    kyc_flag = Column(String(1))
    sub_broker_code = Column(String(15))
    euin_number = Column(String(20))
    euin_declaration = Column(String(1))
    min_redemption_flag = Column(String(1))
    dpc_flag = Column(String(1))
    all_units = Column(String(1))
    redemption_units = Column(String(20))
    sub_broker_arn = Column(String(20))
    bank_ref_no = Column(String(25))
    account_no = Column(String(20))
    mobile_no = Column(String(10))
    email = Column(String(50))
    mandate_id = Column(String(13))
    filler1 = Column(String(50))
    trxn_order_id = Column(String(12))
    trxn_status = Column(String(15))
    trxn_remark = Column(Text)
    member_unique_id = Column(String(25))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
