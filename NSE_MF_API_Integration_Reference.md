# NSE MF (NNF) API Integration Reference

Source: *NSEIL Mutual Fund Service System, Protocol for Non-NEAT Front End, v1.9.8 (August 2026)*. Request/response bodies below are the doc's own samples, cleaned into valid JSON (the PDF has trailing commas, missing commas, wrapped base64 and inline comments). Field-level rules (mandatory/optional, size, allowed values) are in the PDF at the page given for each API.

## Base URLs

| Environment | Base URL |
|---|---|
| UAT | `https://nseinvestuat.nseindia.com` |
| Production | `https://www.nseinvest.com` |

Every endpoint below is `{{API_URL}}` + the path shown.

## Common request headers (all APIs)

| Header | Value |
|---|---|
| `Content-Type` | `application/json` |
| `memberId` | Your member id (the doc sample shows `1`) |
| `Authorization` | `Basic base64(<Login User ID>:<Encrypted Password>)` |

**Encrypted Password:** AES-128 encrypt `API Secret|<random number>` using the **API Member License Key** as the key, with a random alphanumeric `salt` and `iv`. Result = `base64(iv::salt::aes_encrypted_val)`. The doc does not state the cipher mode/padding/key derivation, so confirm those with NSE or their sample code.

**Access rules:** your IP must be whitelisted with NSE against the user, and the user needs the matching role in Member Desk. Failure returns:

```json
{
  "status": "403 FORBIDDEN",
  "error_type": "unauthorized",
  "message": "Invalid authorization header or IP Address not mapped with user."
}
```

## Index

| # | API | Method | Path | PDF page |
|---|---|---|---|---|
| 1 | Order Entry (PUR/RED) Service API | POST | `/nsemfdesk/api/v2/transaction/NORMAL` | 7 |
| 2 | Switch Order Entry Service API | POST | `/nsemfdesk/api/v2/transaction/SWITCH` | 11 |
| 3 | XSIP Registration Service API | POST | `/nsemfdesk/api/v2/registration/product/XSIP` | 14 |
| 4 | (X)SIP Topup Registration Service API | POST | `/nsemfdesk/api/v2/registration/product/SIP_TOPUP` | 19 |
| 5 | SIP Registration Service API | POST | `/nsemfdesk/api/v2/registration/product/SIP` | 21 |
| 6 | STP Registration Service API | POST | `/nsemfdesk/api/v2/registration/product/STP` | 26 |
| 7 | SWP Registration Service API | POST | `/nsemfdesk/api/v2/registration/product/SWP` | 30 |
| 8 | Order Cancellation (Normal / Switch) Service API | POST | `/nsemfdesk/api/v2/cancellation/ORDER_CAN` | 33 |
| 9 | UCC Registration – 183 Column API | POST | `/nsemfdesk/api/v2/registration/CLIENTCOMMON183` | 35 |
| 10 | SIP Cancellation Service API | POST | `/nsemfdesk/api/v2/cancellation/SIP_CAN` | 52 |
| 11 | XSIP Cancellation Service API | POST | `/nsemfdesk/api/v2/cancellation/XSIP_CAN` | 54 |
| 12 | DAILY XSIP Cancellation Service API | POST | `/nsemfdesk/api/v2/cancellation/DAILY_XSIP_CAN` | 56 |
| 13 | STP Cancellation Service API | POST | `/nsemfdesk/api/v2/cancellation/STP_CAN` | 58 |
| 14 | Client Bank Detail API (ADD/DEL) | POST | `/nsemfdesk/api/v2/registration/CLIENTBANKDTL` | 59 |
| 15 | Mandate Registration API | POST | `/nsemfdesk/api/v2/registration/product/MANDATE` | 61 |
| 16 | Scan Mandate Image Upload API | POST | `/nsemfdesk/api/v2/fileupload/MANDATEIMG` | 63 |
| 17 | UTR No Update on Purchase Order API | POST | `/nsemfdesk/api/v2/transaction/UTRUPDATE` | 64 |
| 18 | SIP UMRN Mapping API | POST | `/nsemfdesk/api/v2/registration/SIPUMRN` | 65 |
| 19 | Order Status Reports API | POST | `/nsemfdesk/api/v2/reports/PROV_ORDERS` | 66 |
| 19 | Order Status Reports API | POST | `/nsemfdesk/api/v2/reports/ORDER_STATUS` | 66 |
| 20 | Mandate Status Report API | POST | `/nsemfdesk/api/v2/reports/MANDATE_STATUS` | 70 |
| 21 | Get short URL Link API | POST | `/nsemfdesk/api/v2/reports/GET_LINK` | 71 |
| 22 | Resend Communication API | POST | `/nsemfdesk/api/v2/registration/RESEND_COMM` | 73 |
| 23 | Fatca Upload ( For Individual Only) API | POST | `/nsemfdesk/api/v2/registration/FATCA` | 75 |
| 24 | Fatca Upload (Common) API | POST | `/nsemfdesk/api/v2/registration/FATCA_COMMON` | 83 |
| 25 | AOF Image Upload API | POST | `/nsemfdesk/api/v2/fileupload/AOFIMG` | 93 |
| 26 | FATCA Image Upload API | POST | `/nsemfdesk/api/v2/fileupload/FATCAIMG` | 94 |
| 27 | ELOG Upload API | POST | `/nsemfdesk/api/v2/registration/eLOG` | 95 |
| 28 | POA Upload API | POST | `/nsemfdesk/api/v2/fileupload/POA_UPLOAD` | 97 |
| 29 | Client Cancel Cheque Upload API | POST | `/nsemfdesk/api/v2/fileupload/CANCELCHEQUE` | 98 |
| 30 | Member fund allocation order wise Report API | POST | `/nsemfdesk/api/v2/reports/MEMBER_FUND_ALLOCATION/ORDER_WISE` | 99 |
| 31 | Agewise/Bankwise orders funds received report API | POST | `/nsemfdesk/api/v2/reports/MEMBER_FUND_ALLOCATION/AGE_WISE` | 101 |
| 32 | Redemption Payout Date Report API | POST | `/nsemfdesk/api/v2/reports/REDEMPTION_PAYOUT` | 104 |
| 33 | Redemption Payout Date Report - Non Demat API | POST | `/nsemfdesk/api/v2/reports/REDEMPTION_PAYOUT_NON_DEMAT` | 106 |
| 34 | Redemption Statement Report API | POST | `/nsemfdesk/api/v2/reports/REDEMPTION_STATEMENT` | 108 |
| 35 | Allotment Statement Report API | POST | `/nsemfdesk/api/v2/reports/ALLOTMENT_STATEMENT` | 111 |
| 36 | Securities Delivery and Shortage Service API | POST | `/nsemfdesk/api/v2/reports/SECURITIES_DELIVERY_AND_SHORTAGE_REPORT` | 116 |
| 37 | 2FA Report API | POST | `/nsemfdesk/api/v2/reports/2fa` | 121 |
| 38 | Client Authorization report API | POST | `/nsemfdesk/api/v2/reports/client_authorization` | 123 |
| 39 | Client Detail Report API | POST | `/nsemfdesk/api/v2/reports/CLIENT_DETAIL_REPORT` | 125 |
| 40 | Order Lifecycle Report API | POST | `/nsemfdesk/api/v2/reports/order_lifecycle` | 129 |
| 41 | Transaction Detail Report API | POST | `/nsemfdesk/api/v2/reports/TRANSACTION_DETAIL_REPORT` | 131 |
| 42 | FATCA Report API | POST | `/nsemfdesk/api/v2/reports/FATCA_REPORT` | 136 |
| 43 | AOF Image Upload Report API | POST | `/nsemfdesk/api/v2/reports/AOF_IMAGE_UPLOAD_REPORT` | 139 |
| 44 | eLOG Upload Report API | POST | `/nsemfdesk/api/v2/reports/ELOG_UPLOAD_REPORT` | 141 |
| 45 | SIP Registration Report API | POST | `/nsemfdesk/api/v2/reports/SIP_REG_REPORT` | 143 |
| 46 | SIP Cancellation Report API | POST | `/nsemfdesk/api/v2/reports/SIP_CAN_REPORT` | 145 |
| 47 | SIP Installment Due Report API | POST | `/nsemfdesk/api/v2/reports/SIP_INST_DUE_REPORT` | 146 |
| 48 | SIP Topup Registration Report API | POST | `/nsemfdesk/api/v2/reports/SIP_TOPUP_REPORT` | 148 |
| 49 | Stepup Registration Report API | POST | `/nsemfdesk/api/v2/reports/STEPUP_REG_REPORT` | 149 |
| 50 | XSIP Registration Report API | POST | `/nsemfdesk/api/v2/reports/XSIP_REG_REPORT` | 151 |
| 51 | XSIP Cancellation Report API | POST | `/nsemfdesk/api/v2/reports/XSIP_CAN_REPORT` | 153 |
| 52 | XSIP Installment Due Report API | POST | `/nsemfdesk/api/v2/reports/XSIP_INST_DUE_REPORT` | 154 |
| 53 | XSIP Topup Registration Report API | POST | `/nsemfdesk/api/v2/reports/XSIP_TOPUP_REPORT` | 156 |
| 54 | STP Registration Report API | POST | `/nsemfdesk/api/v2/reports/STP_REG_REPORT` | 157 |
| 55 | STP Cancellation Report API | POST | `/nsemfdesk/api/v2/reports/STP_CAN_REPORT` | 159 |
| 56 | STP Installment Due Report API | POST | `/nsemfdesk/api/v2/reports/STP_INST_DUE_REPORT` | 161 |
| 57 | SWP Registration Report API | POST | `/nsemfdesk/api/v2/reports/SWP_REG_REPORT` | 163 |
| 58 | SWP Cancellation Report API | POST | `/nsemfdesk/api/v2/reports/SWP_CAN_REPORT` | 165 |
| 59 | SWP Installment Due Report API | POST | `/nsemfdesk/api/v2/reports/SWP_INST_DUE_REPORT` | 166 |
| 60 | Scheme Master, NAV & Settlement calendar Download API | POST | `/nsemfdesk/api/v2/reports/MASTER_DOWNLOAD` | 168 |
| 61 | Client KYC Status Report API | POST | `/nsemfdesk/api/v2/reports/CLIENT_KYC_REPORT` | 169 |
| 62 | KYC FRESH REGISTER API | POST | `/nsemfdesk/api/v1/EKYC/EKYCREG` | 170 |
| 63 | Purchase orders payment API | POST | `/nsemfdesk/api/v2/payments/purchase_payment` | 171 |
| 64 | UPI payment status check API | POST | `/nsemfdesk/api/v2/payments/upi_status_check` | 175 |
| 65 | SWP Cancellation Service API | POST | `/nsemfdesk/api/v2/cancellation/SWP_CAN` | 176 |
| 66 | SIP/XSIP Pause Service API | POST | `/nsemfdesk/api/v2/registration/XSIP_PAUSE` | 177 |
| 67 | Client Master report API | POST | `/nsemfdesk/api/v2/reports/client_master_report` | 178 |
| 68 | Change API Secret | POST | `/nsemfdesk/api/v2/admin/CHANGE_API_SECRET` | 184 |
| 69 | Nominee Registration/modification | POST | `/nsemfdesk/api/v1/NFT/NOM` | 184 |
| 70 | Change of Multiple Banks | POST | `/nsemfdesk/api/v1/NFT/COA` | 204 |
| 71 | Change of Dividend | POST | `/nsemfdesk/api/v1/NFT/COD` | 211 |
| 72 | Change of Broker | POST | `/nsemfdesk/api/v1/NFT/COB` | 214 |
| 73 | Change of Contact | POST | `/nsemfdesk/api/v1/NFT/COC` | 218 |
| 74 | Consolidation of Folio | POST | `/nsemfdesk/api/v1/NFT/COF` | 222 |
| 75 | Change of Bank | POST | `/nsemfdesk/api/v1/NFT/COA` | 225 |
| 76 | NFT Image Upload API | POST | `/nsemfdesk/api/v2/fileupload/NFTIMAGE` | 229 |
| 77 | SIP Modification | POST | `/nsemfdesk/api/v2/modification/product/SIP_MOD` | 230 |
| 78 | XSIP Modification | POST | `/nsemfdesk/api/v2/modification/product/XSIP_MOD` | 232 |
| 79 | STP Modification | POST | `/nsemfdesk/api/v2/modification/product/STP_MOD` | 235 |
| 80 | SWP Modification | POST | `/nsemfdesk/api/v2/modification/product/SWP_MOD` | 237 |
| 81 | SIP AMC PAUSE SERVICE API | POST | `/nsemfdesk/api/v2/registration/SIP_AMC_PAUSE` | 240 |
| 82 | SIP AMC PAUSE REPORT API | POST | `/nsemfdesk/api/v2/reports/SIP_AMC_PAUSE` | 241 |

---

## 1. Order Entry (PUR/RED) Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/transaction/NORMAL`  

PDF page: 7

**Sample Request Json**

```json
{
  "transaction_details": [
    {
      "order_ref_number": "",
      "scheme_code": "AXBDGP-GR",
      "trxn_type": "P",
      "buy_sell_type": "FRESH",
      "client_code": "H30350",
      "demat_physical": "C",
      "order_amount": "2000",
      "folio_no": "",
      "remarks": "Order Remark",
      "kyc_flag": "Y",
      "sub_broker_code": "",
      "euin_number": "E123456",
      "euin_declaration": "Y",
      "min_redemption_flag": "N",
      "dpc_flag": "Y",
      "all_units": "N",
      "redemption_units": "",
      "sub_broker_arn": "",
      "bank_ref_no": "5434232",
      "account_no": "343434334",
      "mobile_no": "",
      "email": "",
      "mandate_id": "",
      "filler1": "",
      "member_unique_id": "MUPUR001"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "transaction_details": [
    {
      "order_ref_number": "",
      "scheme_code": "AXBDGP-GR",
      "trxn_type": "P",
      "buy_sell_type": "FRESH",
      "client_code": "H30350",
      "demat_physical": "C",
      "order_amount": "2000",
      "folio_no": "",
      "remarks": "ADD THROUGH API",
      "kyc_flag": "Y",
      "sub_broker_code": "",
      "euin_number": "E123456",
      "euin_declaration": "Y",
      "min_redemption_flag": "N",
      "dpc_flag": "Y",
      "all_units": "N",
      "redemption_units": "",
      "sub_broker_arn": "",
      "bank_ref_no": "5434232",
      "account_no": "343434334",
      "mobile_no": "",
      "email": "",
      "mandate_id": "",
      "filler1": "",
      "trxn_order_id": "432160000001",
      "trxn_status": "TRXN SUCCESS",
      "trxn_remark": "",
      "member_unique_id": "MUPUR001"
    }
  ]
}
```

---

## 2. Switch Order Entry Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/transaction/SWITCH`  

PDF page: 11

**Sample Request Json**

```json
{
  "transaction_details": [
    {
      "order_ref_number": "",
      "from_scheme_code": "RLBPAM-B",
      "to_scheme_code": "RMFCEDP-DP",
      "buy_sell_type": "FRESH",
      "client_code": "h30350",
      "demat_physical": "C",
      "amount": "",
      "units": "10.000",
      "all_units": "N",
      "folio_no": "",
      "remarks": "remarks",
      "kyc_flag": "Y",
      "sub_broker_code": "UCC4790",
      "euin_number": "E123456",
      "euin_declaration": "Y",
      "sub_broker_arn": "",
      "mobile_no": "",
      "email": "",
      "filler1": "",
      "filler2": "",
      "filler3": "",
      "member_unique_id": "MUSWH001"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "transaction_details": [
    {
      "order_ref_number": "",
      "from_scheme_code": "RLBPAM-B",
      "to_scheme_code": "RMFCEDP-DP",
      "buy_sell_type": "FRESH",
      "client_code": "h30350",
      "demat_physical": "C",
      "amount": "",
      "units": "10.000",
      "all_units": "N",
      "folio_no": "",
      "remarks": "remarks",
      "kyc_flag": "Y",
      "sub_broker_code": "UCC4790",
      "euin_number": "E123456",
      "euin_declaration": "Y",
      "sub_broker_arn": "",
      "mobile_no": "",
      "email": "",
      "filler1": "",
      "filler2": "",
      "filler3": "",
      "trxn_so_order_id": "432160000002",
      "trxn_si_order_id": "432160000003",
      "trxn_status": "TRXN SUCCESS",
      "trxn_remark": "",
      "member_unique_id": "MUSWH001"
    }
  ]
}
```

---

## 3. XSIP Registration Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/product/XSIP`  

PDF page: 14

**Sample Request Json**

```json
{
  "reg_data": [
    {
      "amc_code": "AXISMUTUALFUND_MF",
      "sch_code": "AXIOGP-GR",
      "client_code": "H30350",
      "bank_ref_no": "671297212",
      "trans_mode": "D",
      "dp_txn_mode": "C",
      "start_date": "10/08/2023",
      "frequency_type": "MONTHLY",
      "frequency_allowed": "1",
      "installment_amount": "3000",
      "status": "1",
      "member_code": "4079",
      "folio_no": "",
      "sip_remarks": "",
      "installment_no": "12",
      "convenience_fee": "10",
      "xsip_mandate_id": "12",
      "sub_broker_code": "",
      "euin_number": "E399871",
      "euin_declaration": "Y",
      "dpc_flag": "Y",
      "first_order_today": "N",
      "isip_mandate": "",
      "sub_broker_arn": "",
      "end_date": "",
      "primary_holder_mobile": "9574898779",
      "primary_holder_email": "user@gmail.com",
      "step_up_required": "Y",
      "step_up_start_date": "10/09/2023",
      "step_up_end_date": "",
      "step_up_frequency": "semi-annual",
      "step_up_amount": "500",
      "filler_1": "",
      "filler_2": "",
      "filler_3": "",
      "filler_4": "",
      "filler_5": "",
      "member_unique_id": "MUXSIP001"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "amc_code": "AXISMUTUALFUND_MF",
      "sch_code": "AXIOGP-GR",
      "client_code": "H30350",
      "bank_ref_no": "671297212",
      "trans_mode": "D",
      "dp_txn_mode": "C",
      "start_date": "10/08/2023",
      "frequency_type": "MONTHLY",
      "frequency_allowed": "1",
      "installment_amount": "3000",
      "status": "1",
      "member_code": "4079",
      "folio_no": " ",
      "sip_remarks": " ",
      "installment_no": "12",
      "convenience_fee": "10",
      "xsip_mandate_id": "12",
      "sub_broker_code": " ",
      "euin_number": "E399871",
      "euin_declaration": "Y",
      "dpc_flag": "Y",
      "first_order_today": "N",
      "isip_mandate": " ",
      "sub_broker_arn": " ",
      "end_date": " ",
      "primary_holder_mobile": "9574898779",
      "primary_holder_email": "USER@GMAIL.COM",
      "step_up_required": "Y",
      "step_up_start_date": "10/09/2023",
      "step_up_end_date": "",
      "step_up_frequency": "semi-annual",
      "step_up_amount": "500",
      "filler_1": " ",
      "filler_2": " ",
      "filler_3": " ",
      "filler_4": " ",
      "filler_5": " ",
      "reg_id": "202308081000001",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " ",
      "member_unique_id": "MUXSIP001"
    }
  ]
}
```

---

## 4. (X)SIP Topup Registration Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/product/SIP_TOPUP`  

PDF page: 19

> Note: The doc labels the first sample "Response", but it is the request (no reg_id/reg_status/reg_remark). The second one is the real response.

**Sample Request Json (doc labels it "Response")**

```json
{
  "reg_data": [
    {
      "client_code": "K0281",
      "req_type": "SIP",
      "sip_reg_no": 202412021000001,
      "installment_amount": 1000,
      "topup_frequency": "ANNUALLY",
      "topup_amount": 500,
      "start_date": "05/12/2024",
      "end_date": "05/12/2025",
      "internal_ref_no": "",
      "primary_holder_mobile": "9574898779",
      "primary_holder_email": "user@gmail.com"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "K0281",
      "req_type": "SIP",
      "sip_reg_no": 202412021000001,
      "installment_amount": 1000,
      "topup_frequency": "ANNUALLY",
      "topup_amount": 500,
      "start_date": "05/12/2024",
      "end_date": "05/12/2025",
      "internal_ref_no": "",
      "primary_holder_mobile": "9574898779",
      "primary_holder_email": "user@gmail.com",
      "reg_id": "123456",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " "
    }
  ]
}
```

---

## 5. SIP Registration Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/product/SIP`  

PDF page: 21

**Sample Request Json**

```json
{
  "reg_data": [
    {
      "amc_code": "AXISMUTUALFUND_MF",
      "sch_code": "AXIOGP-GR",
      "client_code": "NDI65",
      "internal_ref_no": "671297212",
      "trans_mode": "P",
      "dp_txn_mode": "P",
      "start_date": "08/06/2026",
      "frequency_type": "MONTHLY",
      "frequency_allowed": "1",
      "installment_amount": "3000",
      "status": "1",
      "member_code": "99943",
      "folio_no": "",
      "sip_remarks": "",
      "installment_no": "12",
      "sip_mandate_id": "12",
      "sub_broker_code": "",
      "euin_number": "E399871",
      "euin_declaration": "Y",
      "dpc_flag": "Y",
      "first_order_today": "Y",
      "sub_broker_arn": "",
      "end_date": "",
      "primary_holder_mobile": "",
      "primary_holder_email": "",
      "step_up_required": "",
      "step_up_start_date": "",
      "step_up_end_date": "",
      "step_up_frequency": "",
      "step_up_amout": "",
      "goal_based_sip": "Y",
      "goal_type": "1",
      "goal_name": "MYCAR",
      "goal_amount": "100000.00",
      "filler_1": "",
      "filler_2": "",
      "filler_3": "",
      "filler_4": "",
      "filler_5": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "amc_code": "AXISMUTUALFUND_MF",
      "sch_code": "AXIOGP-GR",
      "client_code": "NDI65",
      "internal_ref_no": "671297212",
      "trans_mode": "P",
      "dp_txn_mode": "P",
      "start_date": "08/06/2026",
      "frequency_type": "MONTHLY",
      "frequency_allowed": "1",
      "installment_amount": "3000",
      "status": "1",
      "member_code": "99943",
      "folio_no": " ",
      "sip_remarks": " ",
      "installment_no": "12",
      "first_order_today": "Y",
      "sub_broker_code": " ",
      "euin_number": "E399871",
      "euin_declaration": "Y",
      "dpc_flag": "Y",
      "sub_broker_arn": " ",
      "end_date": " ",
      "primary_holder_mobile": " ",
      "primary_holder_email": " ",
      "filler_1": " ",
      "filler_2": " ",
      "filler_3": " ",
      "filler_4": " ",
      "filler_5": " ",
      "step_up_required": " ",
      "step_up_start_date": " ",
      "step_up_end_date": " ",
      "step_up_frequency": " ",
      "step_up_amount": " ",
      "send_2fa": " ",
      "send_comm": " ",
      "member_unique_id": " ",
      "goal_based_sip": "Y",
      "goal_type": "1",
      "goal_name": "MYCAR",
      "goal_amount": "100000.00",
      "reg_id": "202605261000011",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " "
    }
  ]
}
```

---

## 6. STP Registration Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/product/STP`  

PDF page: 26

**Sample Request Json**

```json
[
  {
    "client_code": "H30350",
    "from_scheme_code": "PSAD-DR",
    "to_scheme_code": "PSAG-GR",
    "buy_sell_type": "Additional",
    "transaction_mode": "C",
    "folio_no": " ",
    "internal_ref_number": "STP374698",
    "start_date": "28/08/2023",
    "frequency_type": "Monthly",
    "no_of_transfers": "12",
    "to_date": "",
    "installment_amount": "",
    "installment_units": "10",
    "first_order_today": "Y",
    "sub_broker_code": "24542",
    "euin_declaration": "Y",
    "euin_number": "E123456",
    "remarks": "",
    "sub_broker_arn_code": "",
    "mobile": "9892837654",
    "email": "test@gmail.com",
    "member_unique_id": "MUSTP001"
  }
]
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "H30350",
      "from_scheme_code": "PSAD-DR",
      "to_scheme_code": "PSAG-GR",
      "buy_sell_type": "Additional",
      "transaction_mode": "C",
      "folio_no": " ",
      "internal_ref_number": "STP374698",
      "start_date": "28/08/2023",
      "frequency_type": "Monthly",
      "no_of_transfers": "12",
      "to_date": "",
      "installment_amount": "",
      "installment_units": "10",
      "first_order_today": "Y",
      "sub_broker_code": "24542",
      "euin_declaration": "Y",
      "euin_number": "E123456",
      "remarks": "",
      "sub_broker_arn_code": "",
      "mobile": "9892837654",
      "email": "test@gmail.com",
      "reg_id": "202308081000003",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " ",
      "member_unique_id": "MUSTP001"
    }
  ]
}
```

---

## 7. SWP Registration Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/product/SWP`  

PDF page: 30

**Sample Request Json**

```json
{
  "reg_data": [
    {
      "client_code": "K102",
      "scheme_code": "BS41A-DP",
      "trans_mode": "D",
      "folio_no": "9105208524",
      "internal_ref_no": "SWP111112",
      "start_date": "28/08/2023",
      "no_of_withdrawals": "12",
      "frequency_type": "Monthly",
      "installmenamount": "5000",
      "installment_units": "100",
      "first_order_today": "N",
      "sub_broker_code": "1461",
      "euin_declaration": "Y",
      "euin_number": "E213200",
      "remarks": "",
      "sub_broker_arn": "",
      "mobile": "9909011973",
      "email": "ashit.rana@njgroup.in",
      "account_no": "0226564545",
      "member_unique_id": "MUSWP001"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "K102",
      "scheme_code": "BS41A-DP",
      "trans_mode": "D",
      "folio_no": "9105208524",
      "internal_ref_no": "SWP111112",
      "start_date": "28/08/2023",
      "no_of_withdrawals": "12",
      "frequency_type": "Monthly",
      "installmenamount": "5000",
      "installment_units": "100",
      "first_order_today": "N",
      "sub_broker_code": "1461",
      "euin_declaration": "Y",
      "euin_number": "E213200",
      "remarks": "",
      "sub_broker_arn": "",
      "mobile": "9909011973",
      "email": "ashit.rana@njgroup.in",
      "account_no": "0226564545",
      "reg_id": "202308081000004",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " ",
      "member_unique_id": "MUSWP001"
    }
  ]
}
```

---

## 8. Order Cancellation (Normal / Switch) Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/cancellation/ORDER_CAN`  

PDF page: 33

**Sample Request Json**

```json
{
  "can_data": [
    {
      "client_code": "4100030",
      "order_no": "433120000008",
      "remarks": "switch cancel 433110000018"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "4100030",
      "order_no": "433120000008",
      "remarks": "SWITCH CANCEL 433110000018",
      "can_status": "CAN FAILED",
      "can_remark": "CLIENT CODE: 4100030 does not exist."
    }
  ]
}
```

---

## 9. UCC Registration – 183 Column API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/CLIENTCOMMON183`  

PDF page: 35

**Sample Request Json**

```json
{
  "reg_details": [
    {
      "client_code ": "H3034",
      "primary_holder_first_name ": "PRIYANKA",
      "primary_holder_middle_name ": "R",
      "primary_holder_last_name ": "TOPIWALA",
      "tax_status ": "INDIVIDUAL",
      "gender ": "MALE",
      "primary_holder_dob_incorporation ": "04/11/1994",
      "occupation_code ": "BUSINESS",
      "holding_nature ": "SINGLE",
      "second_holder_first_name ": " ",
      "second_holder_middle_name ": " ",
      "second_holder_last_name ": " ",
      "third_holder_first_name ": " ",
      "third_holder_middle_name ": " ",
      "third_holder_last_name ": " ",
      "second_holder_dob ": " ",
      "third_holder_dob ": " ",
      "guardian_first_name ": " ",
      "guardian_middle_name ": " ",
      "guardian_last_name ": " ",
      "guardian_dob ": " ",
      "primary_holder_pan_exempt ": "NO",
      "second_holder_pan_exempt ": " ",
      "third_holder_pan_exempt ": " ",
      "guardian_pan_exempt ": " ",
      "primary_holder_pan ": "BADPT6767G",
      "second_holder_pan ": " ",
      "third_holder_pan ": " ",
      "guardian_pan ": " ",
      "primary_holder_exempt_category ": " ",
      "second_holder_exempt_category ": " ",
      "third_holder_exempt_category ": " ",
      "guardian_exempt_category ": " ",
      "client_type ": "NON DEMAT",
      "pms ": "NO",
      "default_dp ": "PHYS",
      "cdsl_dpid ": " ",
      "cdslcltid ": " ",
      "cmbp_id ": "12345666",
      "nsdldpid ": " ",
      "nsdlcltid ": " ",
      "account_type_1 ": "SB",
      "account_no_1 ": "12311115",
      "micr_no_1 ": " ",
      "ifsc_code_1 ": "SBIN0000019",
      "default_bank_flag_1 ": "NO",
      "account_type_2 ": "SB",
      "account_no_2 ": "12311125",
      "micr_no_2 ": " ",
      "ifsc_code_2 ": "SBIN0000018",
      "default_bank_flag_2 ": "YES",
      "account_type_3 ": " ",
      "account_no_3 ": " ",
      "micr_no_3 ": " ",
      "ifsc_code_3 ": " ",
      "default_bank_flag_3 ": " ",
      "account_type_4 ": " ",
      "account_no_4 ": " ",
      "micr_no_4 ": " ",
      "ifsc_code_4 ": " ",
      "default_bank_flag_4 ": " ",
      "account_type_5 ": " ",
      "account_no_5 ": " ",
      "micr_no_5 ": " ",
      "ifsc_code_5 ": " ",
      "default_bank_flag_5 ": " ",
      "cheque_name ": "MY CHEQUE NAME",
      "div_pay_mode ": "1",
      "address_1 ": "ADDRESS_1",
      "address_2 ": "ADDRESS_2",
      "address_3 ": "ADDRESS_3",
      "city ": "MUMBAI",
      "state ": "MAHARASHTRA",
      "pincode ": "400008",
      "country ": "INDIA",
      "resi_phone ": "123123123",
      "resi_fax ": "321321321",
      "office_phone ": "789789789",
      "office_fax ": "987987987",
      "email ": "RAJU.SINGH@NJGROUP.IN",
      "communication_mode ": "ELECTRONIC",
      "foreign_address_1 ": " ",
      "foreign_address_2 ": " ",
      "foreign_address_3 ": " ",
      "foreign_address_city ": " ",
      "foreign_address_pincode ": " ",
      "foreign_address_state ": " ",
      "foreign_address_country ": " ",
      "foreign_address_resi_phone ": " ",
      "foreign_address_fax ": " ",
      "foreign_address_off_phone ": " ",
      "foreign_address_off_fax ": " ",
      "indian_mobile_no ": "7079093915",
      "primary_holder_kyc_type ": "CKYC COMPLIANT",
      "primary_holder_ckyc_number ": "1234567891",
      "second_holder_kyc_type ": " ",
      "second_holder_ckyc_number ": " ",
      "third_holder_kyc_type ": " ",
      "third_holder_ckyc_number ": " ",
      "guardian_kyc_type ": " ",
      "guardian_ckyc_number ": " ",
      "primary_holder_kra_exempt_ref_no ": " ",
      "second_holder_kra_exempt_ref_no ": " ",
      "third_holder_kra_exempt_ref_no ": " ",
      "guardian_exempt_ref_no ": " ",
      "aadhaar_updated ": "YES",
      "mapin_id ": "1234567887654321",
      "paperless_flag ": "Paper",
      "lei_no": " ",
      "lei_validity": " ",
      "mobile_declaration_flag": "Self",
      "email_declaration_flag": "Self",
      "second_holder_email": " ",
      "second_holder_email_declaration": " ",
      "second_holder_mobile": " ",
      "second_holder_mobile_declaration": " ",
      "third_holder_email": " ",
      "third_holder_email_declaration": " ",
      "third_holder_mobile": " ",
      "third_holder_mobile_declaration": " ",
      "guardian_relation": " ",
      "nomination_opt": "Y",
      "nomination_authentication": "OTP",
      "nominee_1_name ": "NOMINEE 1 NAME",
      "nominee_1_relationship ": "AUNT",
      "nominee_1_applicable ": "90",
      "nominee_1_minor_flag ": "NO",
      "nominee_1_dob ": " ",
      "nominee_1_guardian ": " ",
      "nominee_1_guardian_pan": "FSEPS0104D",
      "nominee_1_identity_type": "1",
      "nominee_1_identity_number": "CCCCC1234C",
      "nominee_1_email": "",
      "nominee_1_mobile": "",
      "nominee_1_address1": "ADDRESS_1",
      "nominee_1_address2": "ADDRESS_2",
      "nominee_1_address3": "ADDRESS_3",
      "nominee_1_city": "MUMBAI",
      "nominee_1_pin": "400008",
      "nominee_1_country": "INDIA",
      "nominee_2_name ": "NOMINEE 2 NAME",
      "nominee_2_relationship ": "AUNT",
      "nominee_2_applicable ": "10",
      "nominee_2_dob ": "01/02/2010",
      "nominee_2_minor_flag ": "YES",
      "nominee_2_guardian ": "NOMINEE 2 GUARDIAN",
      "nominee_2_guardian_pan": "FSEPS0104F",
      "nominee_2_identity_type": "1",
      "nominee_2_identity_number": "BBBBB1234B",
      "nominee_2_email": "",
      "nominee_2_mobile": "",
      "nominee_2_address1": "ADDRESS_1",
      "nominee_2_address2": "ADDRESS_2",
      "nominee_2_address3": "ADDRESS_3",
      "nominee_2_city": "MUMBAI",
      "nominee_2_pin": "400008",
      "nominee_2_country": "INDIA",
      "nominee_3_name ": " ",
      "nominee_3_relationship ": " ",
      "nominee_3_applicable ": "0",
      "nominee_3_dob ": " ",
      "nominee_3_minor_flag ": " ",
      "nominee_3_guardian ": " ",
      "nominee_3_guardian_pan": " ",
      "nominee_3_identity_type": "1",
      "nominee_3_identity_number": "AAAAA1234A",
      "nominee_3_email": "",
      "nominee_3_mobile": "",
      "nominee_3_address1": "ADDRESS_1",
      "nominee_3_address2": "ADDRESS_2",
      "nominee_3_address3": "ADDRESS_3",
      "nominee_3_city": "MUMBAI",
      "nominee_3_pin": "400008",
      "nominee_3_country": "INDIA",
      "nominee_soa": "N",
      "reg_id": "",
      "reg_status": "",
      "reg_remark": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_details": [
    {
      "client_code ": "H3034",
      "primary_holder_first_name ": "PRIYANKA",
      "primary_holder_middle_name ": "R",
      "primary_holder_last_name ": "TOPIWALA",
      "tax_status ": "INDIVIDUAL",
      "gender ": "MALE",
      "primary_holder_dob_incorporation ": "04/11/1994",
      "occupation_code ": "BUSINESS",
      "holding_nature ": "SINGLE",
      "second_holder_first_name ": " ",
      "second_holder_middle_name ": " ",
      "second_holder_last_name ": " ",
      "third_holder_first_name ": " ",
      "third_holder_middle_name ": " ",
      "third_holder_last_name ": " ",
      "second_holder_dob ": " ",
      "third_holder_dob ": " ",
      "guardian_first_name ": " ",
      "guardian_middle_name ": " ",
      "guardian_last_name ": " ",
      "guardian_dob ": " ",
      "primary_holder_pan_exempt ": "NO",
      "second_holder_pan_exempt ": " ",
      "third_holder_pan_exempt ": " ",
      "guardian_pan_exempt ": " ",
      "primary_holder_pan ": "BADPT6767G",
      "second_holder_pan ": " ",
      "third_holder_pan ": " ",
      "guardian_pan ": " ",
      "primary_holder_exempt_category ": " ",
      "second_holder_exempt_category ": " ",
      "third_holder_exempt_category ": " ",
      "guardian_exempt_category ": " ",
      "client_type ": "NON DEMAT",
      "pms ": "NO",
      "default_dp ": "PHYS",
      "cdsl_dpid ": " ",
      "cdslcltid ": " ",
      "cmbp_id ": "12345666",
      "nsdldpid ": " ",
      "nsdlcltid ": " ",
      "account_type_1 ": "SB",
      "account_no_1 ": "12311115",
      "micr_no_1 ": " ",
      "ifsc_code_1 ": "SBIN0000019",
      "default_bank_flag_1 ": "NO",
      "account_type_2 ": "SB",
      "account_no_2 ": "12311125",
      "micr_no_2 ": " ",
      "ifsc_code_2 ": "SBIN0000018",
      "default_bank_flag_2 ": "YES",
      "account_type_3 ": " ",
      "account_no_3 ": " ",
      "micr_no_3 ": " ",
      "ifsc_code_3 ": " ",
      "default_bank_flag_3 ": " ",
      "account_type_4 ": " ",
      "account_no_4 ": " ",
      "micr_no_4 ": " ",
      "ifsc_code_4 ": " ",
      "default_bank_flag_4 ": " ",
      "account_type_5 ": " ",
      "account_no_5 ": " ",
      "micr_no_5 ": " ",
      "ifsc_code_5 ": " ",
      "default_bank_flag_5 ": " ",
      "cheque_name ": "MY CHEQUE NAME",
      "div_pay_mode ": "1",
      "address_1 ": "ADDRESS_1",
      "address_2 ": "ADDRESS_2",
      "address_3 ": "ADDRESS_3",
      "city ": "MUMBAI",
      "state ": "MAHARASHTRA",
      "pincode ": "400008",
      "country ": "INDIA",
      "resi_phone ": "123123123",
      "resi_fax ": "321321321",
      "office_phone ": "789789789",
      "office_fax ": "987987987",
      "email ": "RAJU.SINGH@NJGROUP.IN",
      "communication_mode ": "ELECTRONIC",
      "foreign_address_1 ": " ",
      "foreign_address_2 ": " ",
      "foreign_address_3 ": " ",
      "foreign_address_city ": " ",
      "foreign_address_pincode ": " ",
      "foreign_address_state ": " ",
      "foreign_address_country ": " ",
      "foreign_address_resi_phone ": " ",
      "foreign_address_fax ": " ",
      "foreign_address_off_phone ": " ",
      "foreign_address_off_fax ": " ",
      "indian_mobile_no ": "7079093915",
      "primary_holder_kyc_type ": "CKYC COMPLIANT",
      "primary_holder_ckyc_number ": "1234567891",
      "second_holder_kyc_type ": " ",
      "second_holder_ckyc_number ": " ",
      "third_holder_kyc_type ": " ",
      "third_holder_ckyc_number ": " ",
      "guardian_kyc_type ": " ",
      "guardian_ckyc_number ": " ",
      "primary_holder_kra_exempt_ref_no ": " ",
      "second_holder_kra_exempt_ref_no ": " ",
      "third_holder_kra_exempt_ref_no ": " ",
      "guardian_exempt_ref_no ": " ",
      "aadhaar_updated ": "YES",
      "mapin_id ": "1234567887654321",
      "paperless_flag ": "Paper",
      "lei_no": " ",
      "lei_validity": " ",
      "mobile_declaration_flag": "Self",
      "email_declaration_flag": "Self",
      "second_holder_email": " ",
      "second_holder_email_declaration": " ",
      "second_holder_mobile": " ",
      "second_holder_mobile_declaration": " ",
      "third_holder_email": " ",
      "third_holder_email_declaration": " ",
      "third_holder_mobile": " ",
      "third_holder_mobile_declaration": " ",
      "guardian_relation": " ",
      "nomination_opt": "Y",
      "nomination_authentication": "OTP",
      "nominee_1_name ": "NOMINEE 1 NAME",
      "nominee_1_relationship ": "AUNT",
      "nominee_1_applicable ": "90",
      "nominee_1_minor_flag ": "NO",
      "nominee_1_dob ": " ",
      "nominee_1_guardian ": " ",
      "nominee_1_guardian_pan": "FSEPS0104D",
      "nominee_1_identity_type": "1",
      "nominee_1_identity_number": "CCCCC1234C",
      "nominee_1_email": "",
      "nominee_1_mobile": "",
      "nominee_1_address1": "ADDRESS_1",
      "nominee_1_address2": "ADDRESS_2",
      "nominee_1_address3": "ADDRESS_3",
      "nominee_1_city": "MUMBAI",
      "nominee_1_pin": "400008",
      "nominee_1_country": "INDIA",
      "nominee_2_name ": "NOMINEE 2 NAME",
      "nominee_2_relationship ": "AUNT",
      "nominee_2_applicable ": "10",
      "nominee_2_dob ": "01/02/2010",
      "nominee_2_minor_flag ": "YES",
      "nominee_2_guardian ": "NOMINEE 2 GUARDIAN",
      "nominee_2_guardian_pan": "FSEPS0104F",
      "nominee_2_identity_type": "1",
      "nominee_2_identity_number": "BBBBB1234B",
      "nominee_2_email": "",
      "nominee_2_mobile": "",
      "nominee_2_address1": "ADDRESS_1",
      "nominee_2_address2": "ADDRESS_2",
      "nominee_2_address3": "ADDRESS_3",
      "nominee_2_city": "MUMBAI",
      "nominee_2_pin": "400008",
      "nominee_2_country": "INDIA",
      "nominee_3_name ": " ",
      "nominee_3_relationship ": " ",
      "nominee_3_applicable ": "0",
      "nominee_3_dob ": " ",
      "nominee_3_minor_flag ": " ",
      "nominee_3_guardian ": " ",
      "nominee_3_guardian_pan": " ",
      "nominee_3_identity_type": "1",
      "nominee_3_identity_number": "AAAAA1234A",
      "nominee_3_email": "",
      "nominee_3_mobile": "",
      "nominee_3_address1": "ADDRESS_1",
      "nominee_3_address2": "ADDRESS_2",
      "nominee_3_address3": "ADDRESS_3",
      "nominee_3_city": "MUMBAI",
      "nominee_3_pin": "400008",
      "nominee_3_country": "INDIA",
      "nominee_soa": "N",
      "reg_id": "752789",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " "
    }
  ]
}
```

---

## 10. SIP Cancellation Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/cancellation/SIP_CAN`  

PDF page: 52

**Sample Request Json**

```json
{
  "can_data": [
    {
      "client_code": "1001",
      "sip_reg_no": "1747",
      "remarks": "13:(SIP cancel 1747)"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "1001",
      "sip_reg_no": "1747",
      "remarks": "13:(SIP CANCEL 1747)",
      "can_status": "CAN_FAILED",
      "can_remark": "Invalid SIP registration number"
    }
  ]
}
```

---

## 11. XSIP Cancellation Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/cancellation/XSIP_CAN`  

PDF page: 54

**Sample Request Json**

```json
{
  "can_data": [
    {
      "client_code": "1001",
      "xsip_reg_no": "1747",
      "remarks": "13:(SIP cancel 1747)"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "1001",
      "xsip_reg_no": "1747",
      "remarks": "13:(SIP cancel 1747)",
      "can_status": "CAN_FAILED",
      "can_remark": "Invalid XSIP registration number"
    }
  ]
}
```

---

## 12. DAILY XSIP Cancellation Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/cancellation/DAILY_XSIP_CAN`  

PDF page: 56

**Sample Request Json**

```json
{
  "can_data": [
    {
      "client_code": "1001",
      "xsip_reg_no": "1747",
      "xsip_cancel_date": "25/01/2025",
      "remarks": "13:(SIP cancel 1747)"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "1001",
      "xsip_reg_no": "1747",
      "xsip_cancel_date": "25/01/2025",
      "remarks": "13:(SIP cancel 1747)",
      "can_status": "CAN_FAILED",
      "can_remark": "Invalid XSIP registration number"
    }
  ]
}
```

---

## 13. STP Cancellation Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/cancellation/STP_CAN`  

PDF page: 58

**Sample Request Json**

```json
{
  "can_data": [
    {
      "client_code": "1001",
      "stp_reg_no": "1747",
      "remarks": "STP cancel 1747"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "1001",
      "stp_reg_no": "1747",
      "remarks": "STP CANCEL 1747",
      "can_status": "CAN_FAILED",
      "can_remark": "Invalid STP registration number"
    }
  ]
}
```

---

## 14. Client Bank Detail API (ADD/DEL)

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/CLIENTBANKDTL`  

PDF page: 59

**Sample Request Json**

```json
{
  "bank_dtl": [
    {
      "client_code": "K0281",
      "action_type": "ADD",
      "account_type": "SB",
      "account_no": "311242065229",
      "micr_no": "",
      "ifsc_code": "KKBK0000872"
    },
    {
      "client_code": "A0145",
      "action_type": "DEL",
      "account_type": "CB",
      "account_no": "00101229769449",
      "micr_no": "",
      "ifsc_code": "SBIN0004193",
      "default_bank_flag": "N"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "bank_dtl": [
    {
      "client_code": "K0281",
      "action_type": "ADD",
      "account_type": "SB",
      "account_no": "311242065229",
      "micr_no": "",
      "ifsc_code": "KKBK0000872",
      "status": "SUCCESS",
      "error_remark": ""
    },
    {
      "client_code": "A0145",
      "action_type": "DEL",
      "account_type": "CB",
      "account_no": "00101229769449",
      "micr_no": "",
      "ifsc_code": "SBIN0004193",
      "status": "FAIL",
      "error_remark": "bank not found"
    }
  ]
}
```

---

## 15. Mandate Registration API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/product/MANDATE`  

PDF page: 61

**Sample Request Json**

```json
{
  "reg_data": [
    {
      "client_code": "500231",
      "amount": "100000",
      "mandate_type": "X",
      "account_no": "1234567890",
      "ac_type": "SB",
      "ifsc_code": "SBIN0000018",
      "micr_code": "",
      "start_date": "07/03/2024",
      "end_date": "15/09/2025",
      "member_mandate_no": "112233"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "500231",
      "amount": "100000",
      "mandate_type": "X",
      "account_no": "1234567890",
      "ac_type": "SB",
      "ifsc_code": "SBIN0000018",
      "micr_code": " ",
      "start_date": "07/03/2024",
      "end_date": "15/09/2025",
      "member_mandate_no": "112233",
      "reg_id": "2024030710018",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " "
    }
  ]
}
```

---

## 16. Scan Mandate Image Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/fileupload/MANDATEIMG`  

PDF page: 63

> Note: file_data is base64 of the image.

**Sample Request Json**

```json
{
  "client_code": "K0281",
  "mandate_id": "751518",
  "file_name": "abc.jpg",
  "file_data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
}
```

**Sample Response Json(Success)**

```json
{
  "status": "100",
  "message": "Mandate Uploaded Successfully."
}
```

**Sample Response Json(Failure)**

```json
{
  "status": "101",
  "message": "Image already uploaded."
}
```

---

## 17. UTR No Update on Purchase Order API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/transaction/UTRUPDATE`  

PDF page: 64

**Sample Request Json**

```json
{
  "utr_details": [
    {
      "client_code": "K0281",
      "bank_name": "Kotak Mahindra bank",
      "account_no": "0123456522",
      "ifsc": "KKBK0000872",
      "utr_no": "150983120614",
      "transfer_date": "29/04/2024",
      "order_id": "441200000008"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "utr_details": [
    {
      "client_code": "K0281",
      "bank_name": "Kotak Mahindra bank",
      "account_no": "0123456522",
      "ifsc": "KKBK0000872",
      "utr_no": "150983120614",
      "transfer_date": "29/04/2024",
      "order_id": "441200000008",
      "status": 100,
      "message": ""
    }
  ]
}
```

---

## 18. SIP UMRN Mapping API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/SIPUMRN`  

PDF page: 65

**Sample Request Json**

```json
{
  "sip_reg_id": 202404291005001,
  "umrn": "KBID7010000088990011",
  "remark": "request by member"
}
```

**Sample Response Json**

```json
{
  "sip_reg_id": 202404291005001,
  "umrn": "KBID7010000088990011",
  "remark": "request by member",
  "status": 100,
  "message": ""
}
```

---

## 19. Order Status Reports API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/PROV_ORDERS`  
**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/ORDER_STATUS`  

PDF page: 66

> Note: One request body is shared by both endpoints; the doc gives a separate response sample for each.

**Sample Request Json**

```json
{
  "from_date": "2023-11-10",
  "to_date": "2023-11-16",
  "trans_type": "ALL",
  "order_type": "ALL",
  "sub_order_type": "ALL",
  "client_code": "",
  "order_status": "",
  "settlement_type": "",
  "order_ids": "",
  "instalment_no": "Y",
  "sip_reg_nos": " 202608211027628",
  "member_unique_ids": "",
  "date_type": "REQUEST DATE"
}
```

**Provisional Report (PROV_ORDERS) Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_id": "1000001",
      "request_date": "21/08/2026",
      "order_time": "23:42:21",
      "order_id": "462330435031",
      "settlement_id": "2026158",
      "client_code": "295BAC839A",
      "first_applicant_name": "REEMA SINGH",
      "scheme_code": "RGFMCGP-GR",
      "scheme_name": "INVESCO INDIA MIDCAP FUND - REGULAR PLAN - GROWTH",
      "isin": "INF205K01BC9",
      "transaction_type": "P",
      "amount": "500",
      "quantity": "-",
      "transaction_mode": "PHYSICAL",
      "DP_Folio_No": "-",
      "folio_no": "31048668395",
      "login_id": "admin",
      "order_status": "VALID",
      "order_remark": "PROVISIONAL ORDER",
      "sip_reference_no": "-",
      "settlement_type": "T2",
      "order_type": "XSP",
      "sip_registration_no": "202608211027628",
      "sip_registration_date": "21/08/2026",
      "sub_broker_code": "-",
      "euin_code": "E655722",
      "euin_declaration_flag": "Y",
      "all_units": "N",
      "dpc_flag": "Y",
      "order_sub_type": "NRM",
      "first_order": "Y",
      "investment_type": "FRESH",
      "member_remark": "-",
      "kyc_declaration_flag": "Y",
      "min_redemption_flag": "N",
      "sub_broker_arn_code": "ARN-344715",
      "bank_ref_no": "-",
      "account_no": "-",
      "mobile_no": "-",
      "email": "REEMABIOTECH@GMAIL.COM",
      "mandate_id": "-",
      "second_holder_email": "-",
      "second_holder_mobile": "-",
      "third_holder_email": "-",
      "third_holder_mobile": "-",
      "member_unique_id": " ",
      "instalment_no": "1"
    }
  ]
}
```

**Provisional Report (ORDER_STATUS) Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_id": "1000001",
      "order_date": "15/07/2026",
      "order_time": "06:00:00",
      "order_id": "461912697480",
      "settlement_id": "2026130",
      "client_code": "C50BADF003",
      "first_applicant_name": "JAGRUTI BHAVIN SHAH",
      "scheme_code": "SBNP04-GR",
      "scheme_name": "SUNDARAM MID CAP FUND REGULAR GROWTH",
      "isin": "INF903J01173",
      "transaction_type": "P",
      "amount": "5000",
      "quantity": "0.000",
      "transaction_mode": "PHYSICAL",
      "DP_Folio_No": "501763708220",
      "folio_no": "501763708220",
      "login_id": "admin",
      "order_status": "VALID",
      "order_remark": "ALLOTMENT DONE",
      "sip_reference_no": " ",
      "settlement_type": "T2",
      "order_type": "XSP",
      "sip_registration_no": "202607101036421",
      "sip_registration_date": "10/07/2026",
      "sub_broker_code": " ",
      "euin_code": "E486099",
      "euin_declaration_flag": "Y",
      "all_units": "N",
      "dpc_flag": "Y",
      "order_sub_type": "NRM",
      "first_order": "Y",
      "investment_type": "FRESH",
      "member_remark": " ",
      "kyc_declaration_flag": "Y",
      "min_redemption_flag": "N",
      "sub_broker_arn_code": "ARN-259816",
      "bank_ref_no": " ",
      "account_no": " ",
      "mobile_no": " ",
      "email": "HSSIPLSVCB@GMAIL.COM",
      "mandate_id": "2026070915275",
      "second_holder_email": " ",
      "second_holder_mobile": " ",
      "third_holder_email": " ",
      "third_holder_mobile": " ",
      "member_unique_id": " ",
      "instalment_no": "1"
    }
  ]
}
```

---

## 20. Mandate Status Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/MANDATE_STATUS`  

PDF page: 70

**Sample Request Json**

```json
{
  "mandate_id": "2024012510001",
  "client_code": "K0281",
  "from_date": "2024-01-15",
  "to_date": "2024-01-30",
  "memberMandateIds": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "mandateId": "2024012510001",
      "clientCode": "K0281",
      "clientName": "krushanakant desai",
      "memberCode": "70790",
      "bankName": "HDFC BANK",
      "bankBranch": "KOLKATA - STEPHEN HOUSE BBD BAG",
      "amount": "200000",
      "registrationDate": "25/01/2024",
      "status": "APPROVED",
      "umrnNo": "HDFC7010000088990010",
      "remarks": " ",
      "approvedDate": "27/01/2024",
      "bankAccountNumber": "50100101675862",
      "mandateCollectionType": "ENACH",
      "mandateType": "X",
      "dateOfUpload": " ",
      "startDate": "25/01/2024",
      "endDate": "31/12/2050",
      "memberMandateId": "11",
      "dateOfReupload": " "
    }
  ],
  "error_remark": ""
}
```

---

## 21. Get short URL Link API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/GET_LINK`  

PDF page: 71

**Sample Request Json**

```json
{
  "productType": "PUR",
  "productRefId": "443300100912"
}
```

**Sample Response Json**

```json
{
  "productType": "PUR",
  "productRefId": "443300100912",
  "firstHolderLink": "https://nseinvest.com/mf/51ae3912",
  "secondHolderLink": "",
  "thirdHolderLink": "",
  "errorMessage": ""
}
```

---

## 22. Resend Communication API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/RESEND_COMM`  

PDF page: 73

**Sample Request Json**

```json
{
  "productType": "PUR",
  "productRefId": "443300100912"
}
```

**Sample Response Json**

```json
{
  "productType": "PUR",
  "productRefId": "443300100912",
  "response_status": "S",
  "error_remark": ""
}
```

---

## 23. Fatca Upload ( For Individual Only) API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/FATCA`  

PDF page: 75

**Sample Request Json**

```json
{
  "reg_details": [
    {
      "pan_rp": "BVYPD3824K",
      "pekrn": "avdfert123",
      "inv_name": "MoinTest",
      "dob": "19/02/2019",
      "fr_name": "",
      "sp_name": "",
      "tax_status": "01",
      "data_src": "P",
      "addr_type": "5",
      "po_bir_inc": "Kanbhai",
      "co_bir_inc": "TC",
      "tax_res1": "AU",
      "tpin1": "MOINAU",
      "id1_type": "e1",
      "tax_res2": "",
      "tpin2": "",
      "id2_type": "B",
      "tax_res3": "",
      "tpin3": "",
      "id3_type": "",
      "tax_res4": "",
      "tpin4": "",
      "id4_type": "",
      "srce_wealt": "08",
      "corp_servs": "01",
      "inc_slab": "31",
      "net_worth": "12345678901234567",
      "nw_date": "01/01/2019",
      "pep_flag": "N",
      "occ_code": "44",
      "occ_type": "O",
      "exemp_code": "M",
      "ffi_drnfe": "FFI",
      "giin_no": "12345",
      "spr_entity": "ABC",
      "giin_na": "AF",
      "giin_exemc": "1",
      "nffe_catg": "A",
      "act_nfe_sc": "07",
      "nature_bus": "MOHAMMADHANIFBHAI GULAMMUSTAFA",
      "rel_listed": "TATA",
      "exch_name": "O",
      "ubo_appl": "N",
      "ubo_count": "",
      "ubo_name": "",
      "ubo_pan": "",
      "ubo_nation": "",
      "ubo_add1": "",
      "ubo_add2": "",
      "ubo_add3": "",
      "ubo_city": "",
      "ubo_pin": "",
      "ubo_state": "",
      "ubo_cntry": "",
      "ubo_add_ty": "",
      "ubo_ctr": "",
      "ubo_tin": "",
      "ubo_id_ty": "",
      "ubo_cob": "",
      "ubo_dob": "",
      "ubo_gender": "",
      "ubo_fr_nam": "",
      "ubo_occ": "",
      "ubo_occ_ty": "",
      "ubo_tel": "",
      "ubo_mobile": "",
      "ubo_code": "",
      "ubo_hol_pc": "",
      "sdf_flag": "Y",
      "ubo_df": "N",
      "aadhaar_rp": "",
      "new_change": "",
      "log_name": "Moin Kapadia",
      "filler1": "",
      "filler2": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_details": [
    {
      "pan_rp": "BVYPD3824K",
      "pekrn": "AVDFERT123",
      "inv_name": "MOINTEST",
      "dob": "19/02/2019",
      "fr_name": " ",
      "sp_name": " ",
      "tax_status": "01",
      "data_src": "P",
      "addr_type": "5",
      "po_bir_inc": "KANBHAI",
      "co_bir_inc": "TC",
      "tax_res1": "AU",
      "tpin1": "MOINAU",
      "id1_type": "E1",
      "tax_res2": " ",
      "tpin2": " ",
      "id2_type": "B",
      "tax_res3": " ",
      "tpin3": " ",
      "id3_type": " ",
      "tax_res4": " ",
      "tpin4": " ",
      "id4_type": " ",
      "srce_wealt": "08",
      "corp_servs": "01",
      "inc_slab": "31",
      "net_worth": "12345678901234567",
      "nw_date": "01/01/2019",
      "pep_flag": "N",
      "occ_code": "44",
      "occ_type": "O",
      "exemp_code": "M",
      "ffi_drnfe": "FFI",
      "giin_no": "12345",
      "spr_entity": "ABC",
      "giin_na": "AF",
      "giin_exemc": "1",
      "nffe_catg": "A",
      "act_nfe_sc": "07",
      "nature_bus": "MOHAMMADHANIFBHAI GULAMMUSTAFA",
      "rel_listed": "TATA",
      "exch_name": "O",
      "ubo_appl": "N",
      "ubo_count": " ",
      "ubo_name": " ",
      "ubo_pan": " ",
      "ubo_nation": " ",
      "ubo_add1": " ",
      "ubo_add2": " ",
      "ubo_add3": " ",
      "ubo_city": " ",
      "ubo_pin": " ",
      "ubo_state": " ",
      "ubo_cntry": " ",
      "ubo_add_ty": " ",
      "ubo_ctr": " ",
      "ubo_tin": " ",
      "ubo_id_ty": " ",
      "ubo_cob": " ",
      "ubo_dob": " ",
      "ubo_gender": " ",
      "ubo_fr_nam": " ",
      "ubo_occ": " ",
      "ubo_occ_ty": " ",
      "ubo_tel": " ",
      "ubo_mobile": " ",
      "ubo_code": " ",
      "ubo_hol_pc": " ",
      "sdf_flag": "Y",
      "ubo_df": "N",
      "aadhaar_rp": " ",
      "new_change": " ",
      "log_name": "MOIN KAPADIA",
      "filler1": " ",
      "filler2": " ",
      "reg_id": "491531",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " "
    }
  ]
}
```

---

## 24. Fatca Upload (Common) API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/FATCA_COMMON`  

PDF page: 83

**Sample Request Json**

```json
{
  "reg_details": [
    {
      "pan_rp": "BVYPD3824K",
      "pekrn": "avdfert123",
      "inv_name": "MoinTest",
      "dob": "19/02/2019",
      "fr_name": "",
      "sp_name": "",
      "tax_status": "01",
      "data_src": "P",
      "addr_type": "5",
      "po_bir_inc": "Kanbhai",
      "co_bir_inc": "TC",
      "tax_res1": "AU",
      "tpin1": "MOINAU",
      "id1_type": "e1",
      "tax_res2": "",
      "tpin2": "",
      "id2_type": "B",
      "tax_res3": "",
      "tpin3": "",
      "id3_type": "",
      "tax_res4": "",
      "tpin4": "",
      "id4_type": "",
      "srce_wealt": "08",
      "corp_servs": "01",
      "inc_slab": "31",
      "net_worth": "12345678901234567",
      "nw_date": "01/01/2019",
      "pep_flag": "N",
      "occ_code": "44",
      "occ_type": "O",
      "exemp_code": "M",
      "ffi_drnfe": "FFI",
      "giin_no": "12345",
      "spr_entity": "ABC",
      "giin_na": "AF",
      "giin_exemc": "1",
      "nffe_catg": "A",
      "act_nfe_sc": "07",
      "nature_bus": "MOHAMMADHANIFBHAI GULAMMUSTAFA",
      "rel_listed": "TATA",
      "exch_name": "O",
      "ubo_appl": "N",
      "ubo_count": "",
      "sdf_flag": "Y",
      "ubo_df": "N",
      "aadhaar_rp": "",
      "new_change": "",
      "log_name": "Moin Kapadia",
      "ubo_exch": "",
      "ubo_isin": "",
      "ubo_rel_li": "",
      "npo_form": "",
      "npo_dcl": "",
      "npo_rgno": "",
      "ubo_details": [
        {
          "ubo_name": "MAHESHUBONAME",
          "ubo_pan": "UQOPA1188A",
          "ubo_nation": "IN",
          "ubo_add1": "SURATADDRESS",
          "ubo_add2": "SURATADDRESS",
          "ubo_add3": "SURATADDRESS",
          "ubo_city": "SURAT",
          "ubo_pin": "395010",
          "ubo_state": "GJ",
          "ubo_cntry": "IN",
          "ubo_add_ty": "1",
          "ubo_ctr": "IN",
          "ubo_tin": "982345671",
          "ubo_id_ty": "A",
          "ubo_cob": "IN",
          "ubo_dob": "15-06-1960 00:00:00",
          "ubo_gender": "M",
          "ubo_fr_nam": "UBOFATHER",
          "ubo_occ": "1",
          "ubo_occ_ty": "B ",
          "ubo_tel": "9925899707",
          "ubo_mobile": "9033692510",
          "ubo_code": "C01",
          "ubo_hol_pc": "50",
          "ubo_categ": "SMO",
          "ubo_pep_fl": "N",
          "ubo_email": "",
          "ubo_smo_de": "SMODE"
        },
        {
          "ubo_name": "SURESHUBONAME",
          "ubo_pan": "UROPA1188A",
          "ubo_nation": "IN",
          "ubo_add1": "SURATADDRESS01",
          "ubo_add2": "SURATADDRESS02",
          "ubo_add3": "SURATADDRESS03",
          "ubo_city": "SURAT",
          "ubo_pin": "395010",
          "ubo_state": "GJ",
          "ubo_cntry": "IN",
          "ubo_add_ty": "1",
          "ubo_ctr": "IN",
          "ubo_tin": "992345671",
          "ubo_id_ty": "A",
          "ubo_cob": "IN",
          "ubo_dob": "15-06-1960 00:00:00",
          "ubo_gender": "M",
          "ubo_fr_nam": "UBOFATHER",
          "ubo_occ": "1",
          "ubo_occ_ty": "B ",
          "ubo_tel": "9925899707",
          "ubo_mobile": "9033692510",
          "ubo_code": "C01",
          "ubo_hol_pc": "50",
          "ubo_categ": "SMO",
          "ubo_pep_fl": "N",
          "ubo_email": "",
          "ubo_smo_de": "SMODESS"
        }
      ]
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_details": [
    {
      "pan_rp": "BVYPD3824K",
      "pekrn": "avdfert123",
      "inv_name": "MoinTest",
      "dob": "19/02/2019",
      "fr_name": "",
      "sp_name": "",
      "tax_status": "01",
      "data_src": "P",
      "addr_type": "5",
      "po_bir_inc": "Kanbhai",
      "co_bir_inc": "TC",
      "tax_res1": "AU",
      "tpin1": "MOINAU",
      "id1_type": "e1",
      "tax_res2": "",
      "tpin2": "",
      "id2_type": "B",
      "tax_res3": "",
      "tpin3": "",
      "id3_type": "",
      "tax_res4": "",
      "tpin4": "",
      "id4_type": "",
      "srce_wealt": "08",
      "corp_servs": "01",
      "inc_slab": "31",
      "net_worth": "12345678901234567",
      "nw_date": "01/01/2019",
      "pep_flag": "N",
      "occ_code": "44",
      "occ_type": "O",
      "exemp_code": "M",
      "ffi_drnfe": "FFI",
      "giin_no": "12345",
      "spr_entity": "ABC",
      "giin_na": "AF",
      "giin_exemc": "1",
      "nffe_catg": "A",
      "act_nfe_sc": "07",
      "nature_bus": "MOHAMMADHANIFBHAI GULAMMUSTAFA",
      "rel_listed": "TATA",
      "exch_name": "O",
      "ubo_appl": "N",
      "ubo_count": "",
      "sdf_flag": "Y",
      "ubo_df": "N",
      "aadhaar_rp": "",
      "new_change": "",
      "log_name": "Moin Kapadia",
      "ubo_exch": "",
      "ubo_isin": "",
      "ubo_rel_li": "",
      "npo_form": "",
      "npo_dcl": "",
      "npo_rgno": "",
      "ubo_details": [
        {
          "ubo_name": "MAHESHUBONAME",
          "ubo_pan": "UQOPA1188A",
          "ubo_nation": "IN",
          "ubo_add1": "SURATADDRESS",
          "ubo_add2": "SURATADDRESS",
          "ubo_add3": "SURATADDRESS",
          "ubo_city": "SURAT",
          "ubo_pin": "395010",
          "ubo_state": "GJ",
          "ubo_cntry": "IN",
          "ubo_add_ty": "1",
          "ubo_ctr": "IN",
          "ubo_tin": "982345671",
          "ubo_id_ty": "A",
          "ubo_cob": "IN",
          "ubo_dob": "15-06-1960 00:00:00",
          "ubo_gender": "M",
          "ubo_fr_nam": "UBOFATHER",
          "ubo_occ": "1",
          "ubo_occ_ty": "B ",
          "ubo_tel": "9925899707",
          "ubo_mobile": "9033692510",
          "ubo_code": "C01",
          "ubo_hol_pc": "50",
          "ubo_categ": "SMO",
          "ubo_pep_fl": "N",
          "ubo_email": "",
          "ubo_smo_de": "SMODE"
        },
        {
          "ubo_name": "SURESHUBONAME",
          "ubo_pan": "UROPA1188A",
          "ubo_nation": "IN",
          "ubo_add1": "SURATADDRESS01",
          "ubo_add2": "SURATADDRESS02",
          "ubo_add3": "SURATADDRESS03",
          "ubo_city": "SURAT",
          "ubo_pin": "395010",
          "ubo_state": "GJ",
          "ubo_cntry": "IN",
          "ubo_add_ty": "1",
          "ubo_ctr": "IN",
          "ubo_tin": "992345671",
          "ubo_id_ty": "A",
          "ubo_cob": "IN",
          "ubo_dob": "15-06-1960 00:00:00",
          "ubo_gender": "M",
          "ubo_fr_nam": "UBOFATHER",
          "ubo_occ": "1",
          "ubo_occ_ty": "B ",
          "ubo_tel": "9925899707",
          "ubo_mobile": "9033692510",
          "ubo_code": "C01",
          "ubo_hol_pc": "50",
          "ubo_categ": "SMO",
          "ubo_pep_fl": "N",
          "ubo_email": "",
          "ubo_smo_de": "SMODESS"
        }
      ],
      "reg_id": "491531",
      "reg_status": "REG_SUCCESS",
      "reg_remark": " "
    }
  ]
}
```

---

## 25. AOF Image Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/fileupload/AOFIMG`  

PDF page: 93

**Sample Request Json**

```json
{
  "client_code": "10000002",
  "file_name": "test_101_img.jpg",
  "document_type": "NRM",
  "file_data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII"
}
```

**Sample Response Json**

```json
{
  "message": "Image Uploaded Successfully.",
  "status": "100"
}
```

---

## 26. FATCA Image Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/fileupload/FATCAIMG`  

PDF page: 94

**Sample Request Json**

```json
{
  "file_name": "test_101_img.jpg",
  "pan_no": "ABCPY1234M",
  "file_data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII"
}
```

**Sample Response Json**

```json
{
  "message": "Image Uploaded Successfully.",
  "status": "100"
}
```

---

## 27. ELOG Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/eLOG`  

PDF page: 95

**Sample Request Json**

```json
{
  "client_code": "10016115",
  "primary_holder_pan": "ABCPD1234H",
  "primary_holder_ip_address": "192.168.71.197",
  "primary_holder_log_date": "17-JUL-24 16:10:39",
  "second_holder_pan": "BBCPD1234G",
  "second_holder_ip_address": "192.168.71.197",
  "second_holder_log_date": "17-JUL-24 16:10:39",
  "third_holder_pan": "CBCPD1234I",
  "third_holder_ip_address": "192.168.71.197",
  "third_holder_log_date": "17-JUL-24 16:10:39"
}
```

**Sample Response Json**

```json
{
  "client_code": "10016115",
  "primary_holder_pan": "ABCPD1234H",
  "primary_holder_ip_address": "192.168.71.197",
  "primary_holder_log_date": "17-JUL-24 16:10:39",
  "second_holder_pan": "BBCPD1234G",
  "second_holder_ip_address": "192.168.71.197",
  "second_holder_log_date": "17-JUL-24 16:10:39",
  "third_holder_pan": "CBCPD1234I",
  "third_holder_ip_address": "192.168.71.197",
  "third_holder_log_date": "17-JUL-24 16:10:39",
  "elog_status": "100",
  "elog_status_message": "eLog Uploaded Successfully!!"
}
```

---

## 28. POA Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/fileupload/POA_UPLOAD`  

PDF page: 97

**Sample Request Json**

```json
{
  "client_code": "10000002",
  "file_name": "test_101_img.jpg",
  "file_data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII"
}
```

**Sample Response Json**

```json
{
  "message": "POA Uploaded Successfully.",
  "status": "100"
}
```

---

## 29. Client Cancel Cheque Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/fileupload/CANCELCHEQUE`  

PDF page: 98

**Sample Request Json**

```json
{
  "file_name": "image.png",
  "client_code": "500231",
  "account_no": "3112426522",
  "ifsc": "SBIN0000018",
  "account_type": "CB",
  "file_data": "iVBORw0KGgoAAAANSUhEUgAAAAgAAAAIAQMAAAD+wSzIAAAABlBMVEX///+/v7+jQ3Y5AAAADklEQVQI12P4AIX8EAgALgAD/aNpbtEAAAAASUVORK5CYII"
}
```

**Sample Response Json**

```json
{
  "message": "Cheque Uploaded Successfully.",
  "status": "100"
}
```

---

## 30. Member fund allocation order wise Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/MEMBER_FUND_ALLOCATION/ORDER_WISE`  

PDF page: 99

**Sample Request Json**

```json
{
  "from_date": "10-11-2023",
  "to_date": "10-11-2024",
  "client_code": "",
  "pg_bank_refno": "",
  "order_id": "",
  "pg_agencyid": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "2",
  "report_data": [
    {
      "cfppgbankrefno": "080420241306423594511",
      "order_number": "461630000581",
      "duplicatepgbank": " ",
      "orderprocessduplicatepgbank": " ",
      "importedfilename": "pgmis_08042024_010905.txt",
      "errorremarks": " ",
      "id": "486",
      "utrno": "080420241304067310811",
      "membercode": "04079",
      "clientcode": "H30350",
      "paymentdate": "04/08/2024 13:09:19 PM",
      "totalamount": "10000",
      "totalallocatedamount": "0",
      "remainingamount": "10000",
      "totalsettlementamount": "0",
      "remainingamountsettlement": "10000",
      "totalallotmentamount": "0",
      "remainingaamountallotment": "10000",
      "settlement_number": "202485",
      "settled_flag": "Y",
      "allotment_flag": "Y",
      "clientname": "SIMBENE",
      "bankname": "HDFC BANK",
      "ifsccode": "HDFC0010012",
      "remitteraccountno": "343434334",
      "taxstatus": "INDIVIDUAL",
      "accounttype": "SB",
      "refundamount": " ",
      "refunddate": " ",
      "refundutr": " ",
      "payment_mode": "UPI"
    }
  ],
  "error_remark": ""
}
```

---

## 31. Agewise/Bankwise orders funds received report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/MEMBER_FUND_ALLOCATION/AGE_WISE`  

PDF page: 101

**Sample Request Json**

```json
{
  "date": "30-04-2024",
  "client_code": "",
  "settlement_type": "all",
  "amc_code": "AXISMUTUALFUND_MF",
  "scheme_code": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "2",
  "report_data": [
    {
      "membercode": "04079",
      "date": "30/04/2024",
      "orderno": "440080000030",
      "settlementno": "2024006",
      "settlementtype": "T1",
      "mode_funds_initiated_received": " ",
      "bank_where_funds_received": " ",
      "clientcode": "1009",
      "clientname": "BHAVI DESAI",
      "schemecode": "AXIOGP-GR",
      "schemename": "AXIS CREDIT RISK FUND - GROWTH",
      "isin": "INF846K01PO5",
      "buyvalue": "4000",
      "dp_transaction_mode": "N",
      "dp_folio_no": "IN12345612345668",
      "foliono": " ",
      "entryby": "BHAVI",
      "orderstatus": "INVALID",
      "funds_received_status": "I",
      "date_of_receipt_of_funds": " ",
      "credit_confirmation_on_date": " ",
      "referenceno": " ",
      "groupid": " ",
      "accountno": " ",
      "refund_utr_no": " ",
      "refund_amount": " ",
      "refund_date": " "
    },
    {
      "membercode": "04079",
      "date": "30/04/2024",
      "orderno": "440080000034",
      "settlementno": "2024006",
      "settlementtype": "T1",
      "mode_funds_initiated_received": " ",
      "bank_where_funds_received": " ",
      "clientcode": "1009",
      "clientname": "BHAVI DESAI",
      "schemecode": "AXIOGP-GR",
      "schemename": "AXIS CREDIT RISK FUND - GROWTH",
      "isin": "INF846K01PO5",
      "buyvalue": "4000",
      "dp_transaction_mode": "N",
      "dp_folio_no": "IN12345612345668",
      "foliono": " ",
      "entryby": "BHAVI",
      "orderstatus": "payment_not_initiated",
      "funds_received_status": "C",
      "date_of_receipt_of_funds": " ",
      "credit_confirmation_on_date": " ",
      "referenceno": " ",
      "groupid": " ",
      "accountno": " ",
      "refund_utr_no": " ",
      "refund_amount": " ",
      "refund_date": " "
    }
  ],
  "error_remark": ""
}
```

---

## 32. Redemption Payout Date Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/REDEMPTION_PAYOUT`  

PDF page: 104

**Sample Request Json**

```json
{
  "report_type": "Order Date",
  "from_date": "25-04-2024",
  "to_date": "25-04-2024",
  "amc_code": "",
  "order_id": "441160000046,441160000047",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "2",
  "report_data": [
    {
      "amc_code": "MOF",
      "member_code": "04079",
      "client_code": "H30350",
      "folio_number": " ",
      "rta_scheme_code": "DEGP",
      "scheme_code": "MODEGP-GR",
      "scheme_name": "MOTILAL OSWAL DYNAMIC FUND - GROWTH",
      "first_applicant_name": "SIMBENE",
      "first_applicant_pan": "BSLPA2100D",
      "transaction_type": "R",
      "rta_transaction_no": "440990050028",
      "member_remark": "CAMS REDEMPTION ORDER 500 PER AMC",
      "order_id": "440990050028",
      "order_date": "08 APR 2024",
      "allotted_amount": "50000.0000",
      "stt": "0",
      "tax": " ",
      "funds_payout_date": "09 APR 2024",
      "settlement_type": "T1",
      "settlement_id": "2024069",
      "isin": "INF247L01585",
      "funds_payout_status": "P",
      "funds_transfer_date": " ",
      "account_no": " ",
      "neft_number": " ",
      "reason_for_rejection1": " ",
      "alt_account_no": " ",
      "neft_number2": " ",
      "reason_for_rejection2": " ",
      "final_payout_date_client": " ",
      "date_of_amt_refund_to_amc": " ",
      "neft_rtgs_details_amt_refunded": " ",
      "member_unique_id": "MURED0001"
    },
    {
      "amc_code": "MOF",
      "member_code": "04079",
      "client_code": "H30350",
      "folio_number": " ",
      "rta_scheme_code": "DEGP",
      "scheme_code": "MODEGP-GR",
      "scheme_name": "MOTILAL OSWAL DYNAMIC FUND - GROWTH",
      "first_applicant_name": "SIMBENE",
      "first_applicant_pan": "BSLPA2100D",
      "transaction_type": "R",
      "rta_transaction_no": "440990050029",
      "member_remark": "CAMS REDEMPTION ORDER 500 PER AMC",
      "order_id": "440990050029",
      "order_date": "08 APR 2024",
      "allotted_amount": "50000.0000",
      "stt": "0",
      "tax": " ",
      "funds_payout_date": "09 APR 2024",
      "settlement_type": "T1",
      "settlement_id": "2024069",
      "isin": "INF247L01585",
      "funds_payout_status": "P",
      "funds_transfer_date": " ",
      "account_no": " ",
      "neft_number": " ",
      "reason_for_rejection1": " ",
      "alt_account_no": " ",
      "neft_number2": " ",
      "reason_for_rejection2": " ",
      "final_payout_date_client": " ",
      "date_of_amt_refund_to_amc": " ",
      "neft_rtgs_details_amt_refunded": " ",
      "member_unique_id": "MURED0002"
    }
  ],
  "error_remark": ""
}
```

---

## 33. Redemption Payout Date Report - Non Demat API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/REDEMPTION_PAYOUT_NON_DEMAT`  

PDF page: 106

**Sample Request Json**

```json
{
  "report_type": "Order Date",
  "from_date": "25-04-2024",
  "to_date": "25-04-2024",
  "amc_code": "",
  "order_id": "441160000046,441160000047",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "amc_code": "ABSL",
      "member_code": "00014",
      "client_code": "72349",
      "folio_number": "13678083/49",
      "product_code": "P1565",
      "scheme_code": "ESARQD-DP",
      "scheme_name": "ADITYA BIRLA SUN LIFE EQUITY SAVINGS FUND - DIVPAYOUT",
      "first_applicant_name": "SIMBENE",
      "first_applicant_pan": "DHQPK6568F",
      "transaction_type": "R",
      "rta_transaction_no": "1045062217",
      "member_remark": "REDEMPTION ORDER ENTRY BY SIRAJ",
      "order_id": "441160000047",
      "order_date": "31 JAN 2025",
      "funds_payout_status": "S,T,R",
      "settlement_type": "T3",
      "settlement_id": "2025023",
      "isin": "INF959L01FB2",
      "allotted_amount": "207287.04",
      "payout_desc": "ELECTRONIC PAYMENT",
      "mailed_date": "08/25/2024 12:00:00 AM",
      "despatch_mode": " ",
      "despatch_ref": " ",
      "despatch_status": " ",
      "instrm_no": " ",
      "instrm_bank": "HDFC BANK",
      "payee_acno": "00171050027742",
      "funds_payout_date": "09/15/2024 12:00:00 AM",
      "member_unique_id": ""
    }
  ],
  "error_remark": ""
}
```

---

## 34. Redemption Statement Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/REDEMPTION_STATEMENT`  

PDF page: 108

**Sample Request Json**

```json
{
  "order_ids": "",
  "from_date": "21-03-2024",
  "to_date": "28-03-2024",
  "order_type": "ALL",
  "sub_order_type": "ALL",
  "client_code": "",
  "transaction_type": "",
  "order_status": "",
  "settlement_type": "",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "19999",
  "report_data": [
    {
      "reportdate": "08-04-2024",
      "orderno": "440990080026",
      "settlementype": "T3",
      "settlementid": "2024069",
      "orderdate": "08-04-2024",
      "schemecode": "ESARQD-DP",
      "isin": "INF959L01FB2",
      "amount": "-",
      "qty": "100.000",
      "membercode": "04079",
      "branchcode": "CORPBRANCH",
      "userid": "HIREN",
      "foliono": "-",
      "rtaschemecode": "RTA_SCHEME",
      "rtatransactionno": "440990080026",
      "clientcode": "H30350",
      "clientname": "SIMBENE",
      "beneficiaryid": "1234567812345678",
      "allottednav": "10.0000",
      "allottedqty": "5000.000",
      "allottedamt": "50000.00",
      "validflag": "Y",
      "remarks": "-",
      "stt": "0",
      "dpcflag": "Y",
      "dptrans": "C",
      "ordertype": "NRM",
      "ordersubtype": "SWH",
      "scheme_name": "ADITYA BIRLA SUN LIFE EQUITY SAVINGS FUND - DIVPAYOUT",
      "load_amount": "0",
      "tax_amount": "0",
      "member_unique_id": "MURED0001"
    },
    {
      "reportdate": "08-04-2024",
      "orderno": "440990080024",
      "settlementype": "T3",
      "settlementid": "2024069",
      "orderdate": "08-04-2024",
      "schemecode": "ESARQD-DP",
      "isin": "INF959L01FB2",
      "amount": "-",
      "qty": "100.000",
      "membercode": "04079",
      "branchcode": "CORPBRANCH",
      "userid": "HIREN",
      "foliono": "-",
      "rtaschemecode": "RTA_SCHEME",
      "rtatransactionno": "440990080024",
      "clientcode": "H30350",
      "clientname": "SIMBENE",
      "beneficiaryid": "1234567812345678",
      "allottednav": "10.0000",
      "allottedqty": "5000.000",
      "allottedamt": "50000.00",
      "validflag": "Y",
      "remarks": "-",
      "stt": "0",
      "dpcflag": "Y",
      "dptrans": "C",
      "ordertype": "NRM",
      "ordersubtype": "SWH",
      "scheme_name": "ADITYA BIRLA SUN LIFE EQUITY SAVINGS FUND - DIVPAYOUT",
      "load_amount": "0",
      "tax_amount": "0",
      "member_unique_id": "MURED0002"
    }
  ],
  "error_remark": ""
}
```

---

## 35. Allotment Statement Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/ALLOTMENT_STATEMENT`  

PDF page: 111

**Sample Request Json**

```json
{
  "order_ids": "",
  "from_date": "21-03-2024",
  "to_date": "28-03-2024",
  "order_type": "ALL",
  "sub_order_type": "ALL",
  "client_code": "",
  "transaction_type": "",
  "order_status": "",
  "settlement_type": "",
  "date_type": "ORD_DATE",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "4",
  "report_data": [
    {
      "reportdate": "2025-05-28",
      "orderno": "451480000468",
      "settlementype": "T2",
      "settlementid": "2025105",
      "orderdate": "2025-05-27",
      "schemecode": "UMANC-GR",
      "isin": "INICHIRAGGRW",
      "amount": "1000.00",
      "qty": " ",
      "memberid": "05418",
      "branchcode": "CORPBRANCH",
      "userid": "PARTHVI",
      "foliono": " ",
      "rtaschemecode": "RTAC",
      "rtatransactionno": "451480000468",
      "clientcode": "K101",
      "clientname": "KRUNAL S NAIK",
      "beneficiaryid": "IN12345612345668",
      "allottednav": "10.0000",
      "allottedqty": "1000.0000",
      "allotmentamt": "10000.00",
      "validflag": "Y",
      "remarks": " ",
      "stt": "0",
      "internalreferenceno": " ",
      "ordertype": "NRM",
      "sipregistrationno": " ",
      "sipregdate": " ",
      "subbrokercode": "5656757",
      "euincode": "E123456",
      "euindecl": "Y",
      "dpcflag": "Y",
      "dptrans": "N",
      "ordersubtype": "NRM",
      "schemename": "UNION MANGUM FUND - GROWTH",
      "stampduty": "0",
      "pgbankrefno": "ALLOTMENT1",
      "bankaccno": " ",
      "mobileno": "6666666666",
      "emailid": " ",
      "member_unique_id": "M101"
    },
    {
      "reportdate": "2025-05-28",
      "orderno": "451480000467",
      "settlementype": "MF",
      "settlementid": "2025105",
      "orderdate": "2025-05-27",
      "schemecode": "BSL973D-DP",
      "isin": "INF209K01HV8",
      "amount": "1000.00",
      "qty": " ",
      "memberid": "05418",
      "branchcode": "CORPBRANCH",
      "userid": "PARTHVI",
      "foliono": " ",
      "rtaschemecode": "973D",
      "rtatransactionno": "451480000467",
      "clientcode": "K101",
      "clientname": "KRUNAL S NAIK",
      "beneficiaryid": "IN12345612345668",
      "allottednav": "10.0000",
      "allottedqty": "1000.0000",
      "allotmentamt": "10000.00",
      "validflag": "Y",
      "remarks": " ",
      "stt": "0",
      "internalreferenceno": " ",
      "ordertype": "NRM",
      "sipregistrationno": " ",
      "sipregdate": " ",
      "subbrokercode": "5656757",
      "euincode": "E123456",
      "euindecl": "Y",
      "dpcflag": "Y",
      "dptrans": "N",
      "ordersubtype": "NRM",
      "schemename": "ADITYA BIRLA SUN LIFE EQUITY SAVINGS FUND - DIVPAYOUT",
      "stampduty": "0",
      "pgbankrefno": "ALLOTMENT1",
      "bankaccno": " ",
      "mobileno": "6666666666",
      "emailid": " ",
      "member_unique_id": "M102"
    },
    {
      "reportdate": "2025-05-28",
      "orderno": "451480000466",
      "settlementype": "L0",
      "settlementid": "2025105",
      "orderdate": "2025-05-27",
      "schemecode": "AB153RD-DR-L0",
      "isin": "INF209KA1LJ9",
      "amount": "1000.00",
      "qty": " ",
      "memberid": "05418",
      "branchcode": "CORPBRANCH",
      "userid": "PARTHVI",
      "foliono": " ",
      "rtaschemecode": "153RD",
      "rtatransactionno": "451480000466",
      "clientcode": "K101",
      "clientname": "KRUNAL S NAIK",
      "beneficiaryid": "IN12345612345668",
      "allottednav": "10.0000",
      "allottedqty": "1000.0000",
      "allotmentamt": "10000.00",
      "validflag": "Y",
      "remarks": " ",
      "stt": "0",
      "internalreferenceno": " ",
      "ordertype": "NRM",
      "sipregistrationno": " ",
      "sipregdate": " ",
      "subbrokercode": "5656757",
      "euincode": "E123456",
      "euindecl": "Y",
      "dpcflag": "Y",
      "dptrans": "N",
      "ordersubtype": "NRM",
      "schemename": "ADITYA BIRLA SUN LIFE CASH PLUS - WEEKLY DIVIDEND - REINVESTMENT-REGULAR PLAN",
      "stampduty": "0",
      "pgbankrefno": "ALLOTMENT1",
      "bankaccno": " ",
      "mobileno": "8888888888",
      "emailid": " ",
      "member_unique_id": "12345678901234567890"
    },
    {
      "reportdate": "2025-05-28",
      "orderno": "451480000465",
      "settlementype": "T1",
      "settlementid": "2025105",
      "orderdate": "2025-05-27",
      "schemecode": "ELUSDMR-DR",
      "isin": "INF959L01BG0",
      "amount": "1000.00",
      "qty": " ",
      "memberid": "05418",
      "branchcode": "CORPBRANCH",
      "userid": "PARTHVI",
      "foliono": " ",
      "rtaschemecode": "USDMR",
      "rtatransactionno": "451480000465",
      "clientcode": "K101",
      "clientname": "KRUNAL S NAIK",
      "beneficiaryid": "IN12345612345668",
      "allottednav": "10.0000",
      "allottedqty": "1000.0000",
      "allotmentamt": "10000.00",
      "validflag": "Y",
      "remarks": " ",
      "stt": "0",
      "internalreferenceno": " ",
      "ordertype": "NRM",
      "sipregistrationno": " ",
      "sipregdate": " ",
      "subbrokercode": "5656757",
      "euincode": "E123456",
      "euindecl": "Y",
      "dpcflag": "Y",
      "dptrans": "N",
      "ordersubtype": "NRM",
      "schemename": "ESSEL ULTRA SHORT TERM FUND-DIRECT PLAN MONTHLY DIVIDENDREINVESTMENT",
      "stampduty": "0",
      "pgbankrefno": "ALLOTMENT1",
      "bankaccno": " ",
      "mobileno": "9999999999",
      "emailid": " ",
      "member_unique_id": " "
    }
  ],
  "error_remark": ""
}
```

---

## 36. Securities Delivery and Shortage Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SECURITIES_DELIVERY_AND_SHORTAGE_REPORT`  

PDF page: 116

> Note: The doc prints this URL with the UAT host hard-coded. Use the same `{{API_URL}}` pattern as the other APIs.

**Sample Request Json**

```json
{
  "order_ids": "",
  "member_unique_ids": "",
  "from_date": " 19-01-2026 ",
  "to_date": " 18-02-2026 ",
  "client_code": "700140",
  "settlement_type": "",
  "depository": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "9",
  "report_data": [
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "19-01-2026",
      "sett_no": "2026013",
      "order_no": "460190000289",
      "isin": "INF200K01W80",
      "amount": "1000",
      "alloted_units": "100.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "100.000",
      "date_of_delivery": "22-01-2026 18:06:20",
      "sett_type": "L0",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "78692270220260000027"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "19-01-2026",
      "sett_no": "2026013",
      "order_no": "460190000290",
      "isin": "INF959L01BB1",
      "amount": "1000",
      "alloted_units": "100.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "100.000",
      "date_of_delivery": "22-01-2026 18:06:20",
      "sett_type": "L0",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "78692270220260000018"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "19-01-2026",
      "sett_no": "2026013",
      "order_no": "460190000291",
      "isin": "INF917K01270",
      "amount": "1000",
      "alloted_units": "100.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "100.000",
      "date_of_delivery": "22-01-2026 18:06:20",
      "sett_type": "L0",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "78692270220260000028"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "19-01-2026",
      "sett_no": "2026013",
      "order_no": "460190000292",
      "isin": "INF209K01330",
      "amount": "1000",
      "alloted_units": "100.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "100.000",
      "date_of_delivery": "22-01-2026 18:24:19",
      "sett_type": "T3",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "78692270220260000022"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "19-01-2026",
      "sett_no": "2026013",
      "order_no": "460200000163",
      "isin": "INF846K01PO5",
      "amount": "1000",
      "alloted_units": "100.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "NA",
      "date_of_delivery": "NA",
      "sett_type": "L0",
      "cdsl_shortage": "100.000",
      "nsdl_shortage": "NA",
      "shortage_delivered": "100.000",
      "shortage_settlement_no": "2026014",
      "shortage_date_of_delivery": "20-01-2026 19:40:51",
      "remarks": " ",
      "member_unique_id": "78692270220260000013"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "20-01-2026",
      "sett_no": "2026014",
      "order_no": "460200000164",
      "isin": "INF846K01PO5",
      "amount": "1000",
      "alloted_units": "90.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "90.000",
      "date_of_delivery": "20-01-2026 19:40:51",
      "sett_type": "L0",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "78692270220260000015"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "20-01-2026",
      "sett_no": "2026014",
      "order_no": "460200000171",
      "isin": "INF247L01841",
      "amount": "1000",
      "alloted_units": "101.001",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "NA",
      "date_of_delivery": "NA",
      "sett_type": "L0",
      "cdsl_shortage": "101.001",
      "nsdl_shortage": "NA",
      "shortage_delivered": "0.000",
      "shortage_settlement_no": " ",
      "shortage_date_of_delivery": " ",
      "remarks": " ",
      "member_unique_id": " "
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "20-01-2026",
      "sett_no": "2026014",
      "order_no": "460200000173",
      "isin": "INF247L01817",
      "amount": "1000",
      "alloted_units": "95.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "95.000",
      "date_of_delivery": "20-01-2026 19:40:51",
      "sett_type": "L0",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "78692270220260000016"
    },
    {
      "type": "TRADE",
      "member_code": "78692",
      "order_date": "06-02-2026",
      "sett_no": "2026027",
      "order_no": "460370000766",
      "isin": "INF959L01BB1",
      "amount": "1000",
      "alloted_units": "100.000",
      "nav": "10",
      "depository": "CDSL",
      "dpc": "Y",
      "account_no": "1234567812345678",
      "units_delivered": "100.000",
      "date_of_delivery": "06-02-2026 19:37:16",
      "sett_type": "L0",
      "cdsl_shortage": "0",
      "nsdl_shortage": "NA",
      "shortage_delivered": "NA",
      "shortage_settlement_no": "NA",
      "shortage_date_of_delivery": "NA",
      "remarks": " ",
      "member_unique_id": "7869227022026000M051"
    }
  ],
  "error_remark": ""
}
```

---

## 37. 2FA Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/2fa`  

PDF page: 121

**Sample Request Json**

```json
{
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "product_type": "PUR",
  "product_id": "",
  "client_code": "K123, P147"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "type": "",
      "product_type": "PUR",
      "product_id": "450170000001",
      "product_reg_datetime": "28/12/2024 15:30:45",
      "member_name": "abc member",
      "member_code": "00123",
      "client_code": "K123",
      "primary_holder_name": "krushnakant",
      "mode_of_holding": "SI",
      "folio_no": "",
      "primary_holder_mobile": "8154900000",
      "primary_holder_email": "krushnakant@gmail.com",
      "primary_holder_authentication_datetime": "28/12/2024 18:00:00",
      "primary_holder_authentication_status": "SUCCESS",
      "primary_holder_reply_time": "18:00:00",
      "second_holder_name": "",
      "second_holder_mobile": "",
      "second_holder_email": "",
      "second_holder_authentication_datetime": "",
      "second_holder_authentication_status": "",
      "second_holder_reply_time": "",
      "third_holder_name": "",
      "third_holder_mobile": "",
      "third_holder_email": "",
      "third_holder_authentication_datetime": "",
      "third_holder_authentication_status": "",
      "third_holder_reply_time": ""
    }
  ],
  "error_remark": ""
}
```

---

## 38. Client Authorization report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/client_authorization`  

PDF page: 123

**Sample Request Json**

```json
{
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "client_code": "K123",
  "auth_status": "PENDING",
  "date_type": "AUTH_SENT_DATE"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "auth_email_sent": "Y",
      "auth_status": "SUCCESS",
      "member_code": "00123",
      "client_code": "K123",
      "primary_holder_name": "krushnakant",
      "primary_holder_dob": "01/01/1980",
      "tax_status": "01",
      "gender": "M",
      "holding_nature": "SI",
      "second_holder_name": "",
      "third_holder_name": "",
      "guardian_name": "",
      "primary_holder_pan": "KRUSH1234N",
      "primary_holder_kyc_status": "SUCCESS",
      "primary_holder_kyc_status_remarks": "VERIFIED",
      "second_holder_pan": "",
      "second_holder_kyc_status": "",
      "second_holder_kyc_status_remarks": "",
      "third_holder_pan": "",
      "third_holder_kyc_status": "",
      "third_holder_kyc_status_remarks": "",
      "guardian_pan": "",
      "created_by": "12301",
      "created_at": "28/12/2024 18:20:00",
      "first_holder_fatca_exists": "Y",
      "first_holder_fatca_remarks": "Successful",
      "first_holder_aof_exists": "Y",
      "first_holder_aof_elog_remarks": "Successful",
      "first_holder_elog_exists": "N",
      "first_holder_email": "krushnakant@gmail.com",
      "first_holder_mobile_no": "8154900000",
      "first_holder_auth_status": "SUCCESS",
      "first_holder_auth_remarks": "",
      "first_holder_auth_datetime": "29/12/2024 10:20:00",
      "second_holder_fatca_exists": "",
      "second_holder_fatca_remarks": "",
      "second_holder_aof_exists": "",
      "second_holder_aof_elog_remarks": "",
      "second_holder_elog_exists": "",
      "second_holder_email": "",
      "second_holder_mobile_no": "",
      "second_holder_auth_status": "",
      "second_holder_auth_remarks": "",
      "second_holder_auth_datetime": "",
      "third_holder_fatca_exists": "",
      "third_holder_fatca_remarks": "",
      "third_holder_aof_exists": "",
      "third_holder_aof_elog_remakrs": "",
      "third_holder_elog_exists": "",
      "third_holder_email": "",
      "third_holder_mobile_no": "",
      "third_holder_auth_status": "",
      "third_holder_auth_remarks": "",
      "third_holder_auth_datetime": "",
      "demat_status": "ACTIVE",
      "dp_remarks": "UNDER PROCESS",
      "default_dp": "CDSL",
      "cdsl_dpid": "12064000",
      "cdsl_cltid": "12345678",
      "cmbp_id": "",
      "nsdl_dpid": "",
      "nsdl_cltid": "",
      "bank1_account_type": "SB",
      "bank1_account_no": "1122334455",
      "bank1_name": "SBI BANK",
      "bank1_ifsc": "SBIN00004193",
      "bank1_status": "ACTIVE",
      "bank1_rejection_remarks": "",
      "bank2_account_type": "",
      "bank2_account_no": "",
      "bank2_name": "",
      "bank2_ifsc": "",
      "bank2_status": "",
      "bank2_rejection_remarks": "",
      "bank3_account_type": "",
      "bank3_account_no": "",
      "bank3_name": "",
      "bank3_ifsc": "",
      "bank3_status": "",
      "bank3_rejection_remarks": "",
      "bank4_account_type": "",
      "bank4_account_no": "",
      "bank4_name": "",
      "bank4_ifsc": "",
      "bank4_status": "",
      "bank4_rejection_remarks": "",
      "bank5_account_type": "",
      "bank5_account_no": "",
      "bank5_name": "",
      "bank5_ifsc": "",
      "bank5_status": "",
      "bank5_rejection_remarks": ""
    }
  ],
  "error_remark": ""
}
```

---

## 39. Client Detail Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/CLIENT_DETAIL_REPORT`  

PDF page: 125

**Sample Request Json**

```json
{
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "client_code": "K123",
  "auth_status": "PENDING",
  "date_type": "AUTH_SENT_DATE"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "auth_email_sent": "N",
      "auth_status": "-",
      "member_code": "10",
      "client_code": "K123",
      "migrated_ucc": "N",
      "ucc_status": "Inactive",
      "ucc_remediation": "FATCA Upload is pending",
      "primary_holder_name": "KRUSHNAKANT B DESAI",
      "primary_holder_dob": "13/03/1992",
      "tax_status": "INDIVIDUAL",
      "gender": "MALE",
      "holding_nature": "SINGLE",
      "second_holder_name": " ",
      "third_holder_name": " ",
      "guardian_name": " ",
      "primary_holder_pan": "SHAPS1324F",
      "primary_holder_kyc_checked": "N",
      "primary_holder_kyc_status": " - ",
      "primary_holder_kyc_status_remarks": " ",
      "second_holder_pan": " ",
      "second_holder_kyc_checked": "N",
      "second_holder_kyc_status": " ",
      "second_holder_kyc_status_remarks": " ",
      "third_holder_pan": " ",
      "third_holder_kyc_checked": "N",
      "third_holder_kyc_status": " ",
      "third_holder_kyc_status_remarks": " ",
      "guardian_pan": " ",
      "created_by": "555",
      "created_at": "01/09/2025 12:37:23",
      "first_holder_fatca_exists": "N",
      "first_holder_fatca_image_exists": "N",
      "first_holder_fatca_cams_upload_status": " ",
      "first_holder_fatca_cams_response_status": " ",
      "first_holder_fatca_cams_remarks": " ",
      "first_holder_fatca_kfin_upload_status": " ",
      "first_holder_fatca_kfin_response_status": " ",
      "first_holder_fatca_kfin_remarks": " ",
      "first_holder_normal_aof_exists": "N",
      "first_holder_normal_aof_cams_upload_status": " ",
      "first_holder_normal_aof_cams_response_status": " ",
      "first_holder_normal_aof_cams_remarks": " ",
      "first_holder_normal_aof_kfin_upload_status": " ",
      "first_holder_normal_aof_kfin_response_status": " ",
      "first_holder_normal_aof_kfin_remarks": " ",
      "first_holder_direct_aof_exists": "N",
      "first_holder_direct_aof_cams_upload_status": " ",
      "first_holder_direct_aof_cams_response_status": " ",
      "first_holder_direct_aof_cams_remarks": " ",
      "first_holder_direct_aof_kfin_upload_status": " ",
      "first_holder_direct_aof_kfin_response_status": " ",
      "first_holder_direct_aof_kfin_remarks": " ",
      "first_holder_eLog_exists": "N",
      "first_holder_eLog_cams_upload_status": " ",
      "first_holder_eLog_cams_response_status": " ",
      "first_holder_eLog_cams_remarks": " ",
      "first_holder_eLog_kfin_upload_status": " ",
      "first_holder_eLog_kfin_response_status": " ",
      "first_holder_eLog_kfin_remarks": " ",
      "first_holder_email": "KRUSHNAKANT.ABC@GMAIL.COM",
      "first_holder_mobile_no": "9426648140",
      "first_holder_auth_status": " ",
      "first_holder_auth_remarks": " ",
      "first_holder_auth_datetime": " ",
      "second_holder_fatca_exists": " ",
      "second_holder_fatca_image_exists": " ",
      "second_holder_fatca_cams_upload_status": " ",
      "second_holder_fatca_cams_response_status": " ",
      "second_holder_fatca_cams_remarks": " ",
      "second_holder_fatca_kfin_upload_status": " ",
      "second_holder_fatca_kfin_response_status": " ",
      "second_holder_fatca_kfin_remarks": " ",
      "second_holder_normal_aof_exists": " ",
      "second_holder_normal_aof_cams_upload_status": " ",
      "second_holder_normal_aof_cams_response_status": " ",
      "second_holder_normal_aof_cams_remarks": " ",
      "second_holder_normal_aof_kfin_upload_status": " ",
      "second_holder_normal_aof_kfin_response_status": " ",
      "second_holder_normal_aof_kfin_remarks": " ",
      "second_holder_direct_aof_exists": " ",
      "second_holder_direct_aof_cams_upload_status": " ",
      "second_holder_direct_aof_cams_response_status": " ",
      "second_holder_direct_aof_cams_remarks": " ",
      "second_holder_direct_aof_kfin_upload_status": " ",
      "second_holder_direct_aof_kfin_response_status": " ",
      "second_holder_direct_aof_kfin_remarks": " ",
      "second_holder_eLog_exists": " ",
      "second_holder_eLog_cams_upload_status": " ",
      "second_holder_eLog_cams_response_status": " ",
      "second_holder_eLog_cams_remarks": " ",
      "second_holder_eLog_kfin_upload_status": " ",
      "second_holder_eLog_kfin_response_status": " ",
      "second_holder_eLog_kfin_remarks": " ",
      "second_holder_email": " ",
      "second_holder_mobile_no": " ",
      "second_holder_auth_status": " ",
      "second_holder_auth_remarks": " ",
      "second_holder_auth_datetime": " ",
      "third_holder_fatca_exists": " ",
      "third_holder_fatca_image_exists": " ",
      "third_holder_fatca_cams_upload_status": " ",
      "third_holder_fatca_cams_response_status": " ",
      "third_holder_fatca_cams_remarks": " ",
      "third_holder_fatca_kfin_upload_status": " ",
      "third_holder_fatca_kfin_response_status": " ",
      "third_holder_fatca_kfin_remarks": " ",
      "third_holder_normal_aof_exists": " ",
      "third_holder_normal_aof_cams_upload_status": " ",
      "third_holder_normal_aof_cams_response_status": " ",
      "third_holder_normal_aof_cams_remarks": " ",
      "third_holder_normal_aof_kfin_upload_status": " ",
      "third_holder_normal_aof_kfin_response_status": " ",
      "third_holder_normal_aof_kfin_remarks": " ",
      "third_holder_direct_aof_exists": " ",
      "third_holder_direct_aof_cams_upload_status": " ",
      "third_holder_direct_aof_cams_response_status": " ",
      "third_holder_direct_aof_cams_remarks": " ",
      "third_holder_direct_aof_kfin_upload_status": " ",
      "third_holder_direct_aof_kfin_response_status": " ",
      "third_holder_direct_aof_kfin_remarks": " ",
      "third_holder_eLog_cams_upload_status": " ",
      "third_holder_eLog_cams_response_status": " ",
      "third_holder_eLog_cams_remarks": " ",
      "third_holder_eLog_kfin_upload_status": " ",
      "third_holder_eLog_kfin_response_status": " ",
      "third_holder_eLog_kfin_remarks": " ",
      "third_holder_eLog_exists": " ",
      "third_holder_email": " ",
      "third_holder_mobile_no": " ",
      "third_holder_auth_status": " ",
      "third_holder_auth_remarks": " ",
      "third_holder_auth_datetime": " ",
      "demat_status": "ACTIVE",
      "dp_remarks": " ",
      "default_dp": "PHYS",
      "cdsl_dpid": " ",
      "cdsl_cltid": " ",
      "cmbp_id": " ",
      "nsdl_dpid": " ",
      "nsdl_cltid": " ",
      "bank1_account_type": "CB",
      "bank1_account_no": "734523651",
      "bank1_name": "CENTRAL BANK OF INDIA",
      "bank1_ifsc": "CBIN0282978",
      "bank1_status": "PENDING",
      "bank1_rejection_remarks": " ",
      "bank2_account_type": " ",
      "bank2_account_no": " ",
      "bank2_name": " ",
      "bank2_ifsc": " ",
      "bank2_status": " ",
      "bank2_rejection_remarks": " ",
      "bank3_account_type": " ",
      "bank3_account_no": " ",
      "bank3_name": " ",
      "bank3_ifsc": " ",
      "bank3_status": " ",
      "bank3_rejection_remarks": " ",
      "bank4_account_type": " ",
      "bank4_account_no": " ",
      "bank4_name": " ",
      "bank4_ifsc": " ",
      "bank4_status": " ",
      "bank4_rejection_remarks": " ",
      "bank5_account_type": " ",
      "bank5_account_no": " ",
      "bank5_name": " ",
      "bank5_ifsc": " ",
      "bank5_status": " ",
      "bank5_rejection_remarks": " "
    }
  ],
  "error_remark": ""
}
```

---

## 40. Order Lifecycle Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/order_lifecycle`  

PDF page: 129

**Sample Request Json**

```json
{
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "Product_type": "PUR",
  "product_id": "",
  "client_code": "K123, P147"
}
```

**Sample Response Json**

```json
{
  "type": "",
  "product_type": "PUR",
  "product_id": "450170000001",
  "product_reg_datetime": "28/12/2024 15:30:45",
  "member_name": "abc member",
  "member_code": "00123",
  "client_code": "K123",
  "primary_holder_name": "krushnakant",
  "mode_of_holding": "SI",
  "folio_no": "",
  "primary_holder_mobile": "8154900000",
  "primary_holder_email": "krushnakant@gmail.com",
  "primary_holder_authentication_datetime": "28/12/2024 18:00:00",
  "primary_holder_authentication_status": "SUCCESS",
  "primary_holder_reply_time": "18:00:00",
  "second_holder_name": "",
  "second_holder_mobile": "",
  "second_holder_email": "",
  "second_holder_authentication_datetime": "",
  "second_holder_authentication_status": "",
  "second_holder_reply_time": "",
  "third_holder_name": "",
  "third_holder_mobile": "",
  "third_holder_email": "",
  "third_holder_authentication_datetime": "",
  "third_holder_authentication_status": "",
  "third_holder_reply_time": "",
  "mode_of_payment": "UPI",
  "payment_account_no": "1122334455",
  "payment_datetime": "28/12/2024 19:20:00",
  "payment_status": "SUCCESS",
  "payment_reference_number": "UPI123456",
  "redemption_payment_account_type": "",
  "redemption_payout_account_number": "",
  "redemption_payout_amount": "",
  "redemption_payout_datetime": "",
  "redemption_payment_entity": "",
  "settlement_number": "2024250",
  "reconciliation_datetime": "28/12/2024 19:21:00",
  "reconciliation_status": "SUCCESS",
  "order_status": "VALID",
  "order_remark": "",
  "refund_date": "",
  "refund_amount": "",
  "refund_account_number": "",
  "refund_status": "",
  "refund_reference_number": "",
  "mandate_id": "",
  "mandate_registration_datetime": "",
  "mandate_authorization_datetime": "",
  "mandate_amount": "",
  "mandate_type": "",
  "mandate_bank_name": "",
  "mandate_bank_account_number": "",
  "mandate_ifsc": "",
  "mandate_from_date": "",
  "mandate_to_date": "",
  "mandate_status": "",
  "mandate_umrn": ""
}
```

---

## 41. Transaction Detail Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/TRANSACTION_DETAIL_REPORT`  

PDF page: 131

**Sample Request Json**

```json
{
  "from_date": "01-12-2024",
  "to_date": "07-12-2024",
  "client_code": "1009",
  "applicant_name": "desai",
  "pan": "DDDPD2789A",
  "order_id": "443410000007",
  "systematic_reg_id": "202412061000007,202412061000008",
  "date_type": "REQUEST_DATE"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "99943",
      "client_code": "NDI65",
      "mode_of_holding": "SI",
      "tax_status": "01-INDIVIDUAL",
      "primary_holder_name": "ANKUSH V",
      "primary_holder_pan": "ASDPN5241P",
      "product_type": "NORMAL PURCHASE",
      "product_id": "453530000107",
      "product_reg_date_time": "19-12-2025 16:22:08",
      "frequency": " ",
      "sip_registration_no": " ",
      "transaction_type": "NON DEMAT",
      "sub_broker_code": "987654",
      "sub_broker_arn": "ARN-12345",
      "euin": "E123456",
      "amc_name": "SBI AMC",
      "rta_name": "CAMS",
      "scheme_name_from": "SBI - DYNAMIC BOND FUND - IDCWPAYOUT",
      "scheme_code_from": "SB074D-DP",
      "scheme_name_to": " ",
      "scheme_code_to": " ",
      "dp_folio_no": " ",
      "amount_units": "5040.00(A)",
      "primary_holder_mobile": "985236585",
      "primary_holder_email": "SARITAN@NSE.CO.IN",
      "primary_holder_auth_mode": "EMAIL",
      "primary_holder_auth_status": "SUCCESS",
      "primary_holder_auth_date_time": "19-12-2025 16:23:25",
      "second_holder_name": " ",
      "second_holder_pan": " ",
      "secondary_holder_mobile": " ",
      "secondary_holder_email": " ",
      "secondary_holder_auth_mode": " ",
      "secondary_holder_auth_status": " ",
      "secondary_holder_auth_date_time": " ",
      "third_holder_name": " ",
      "third_holder_pan": " ",
      "third_holder_mobile": " ",
      "third_holder_email": " ",
      "third_holder_auth_mode": " ",
      "third_holder_auth_status": " ",
      "third_holder_auth_date_time": " ",
      "mode_of_payment": "ACH",
      "payin_slip_no": " ",
      "payment_bank_name": "HDFC BANK",
      "payment_account_no": "125632541841500",
      "payment_mandate_id": "2025071410001",
      "payment_account_ifsc": "HDFC0000060",
      "payment_umrn": "HDFC410001",
      "payment_date_time": " ",
      "payment_status": " ",
      "payment_reference_no": " ",
      "reconciliation_status": " ",
      "reconciliation_date_time": " ",
      "pg_mis_utr_no": " ",
      "amc_fund_payout_date_time": " ",
      "amc_payout_utr_no": " ",
      "order_status": "VALID",
      "order_remark": "PAYMENT CONFIRMATION PENDING",
      "rta_rejection_date": " ",
      "alloted_nav": " ",
      "alloted_unit": " ",
      "alloted_amount": " ",
      "stt": " ",
      "folio_no": " ",
      "refund_date": " ",
      "refund_amount": " ",
      "refund_account_number": " ",
      "refund_account_status": " ",
      "refund_reference_number": " ",
      "redemption_payment_account_type": " ",
      "redemption_payout_account_number": " ",
      "redemption_payout_amount": " ",
      "redemption_payout_date_time": " ",
      "redemption_payment_entity": " ",
      "neft_number": " ",
      "entry_by": "ADMIN"
    }
  ],
  "error_remark": ""
}
```

---

## 42. FATCA Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/FATCA_REPORT`  

PDF page: 136

**Sample Request Json**

```json
{
  "pan_pkern_no": "DDDPD1234D",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "pan_rp": "DDDPD1234D",
      "pekrn": "NTND006",
      "inv_name": "PRITEX M PRAJAPATI",
      "dob": "21/09/1990",
      "fr_name": "MANOJBHAI",
      "sp_name": "ROSHANI",
      "tax_status": "01",
      "data_src": "P",
      "addr_type": "1",
      "po_bir_inc ": "IN",
      "co_bir_inc": "IN",
      "tax_res1": "IN",
      "tpin1": "DDDPD1234D",
      "id1_type": "C",
      "tax_res2": " ",
      "tpin2": " ",
      "id2_type": " ",
      "tax_res3": " ",
      "tpin3": " ",
      "id3_type": " ",
      "tax_res4": " ",
      "tpin4": " ",
      "id4_type": " ",
      "srce_wealt": "01",
      "corp_servs": "01",
      "inc_slab": "31",
      "net_worth": "15000",
      "nw_date": "21/07/1990",
      "pep_flag": "Y",
      "occ_code": "01",
      "occ_type": "B",
      "exemp_code": "N",
      "ffi_drnfe": "FFI",
      "giin_no": "FFI",
      "spr_entity": "MUNAFSPONSORINGENTITY",
      "giin_na": "AF",
      "giin_exemc": "11",
      "nffe_catg": "A",
      "act_nfe_sc": "01",
      "nature_bus": "NATUREOFACTIVENFE",
      "rel_listed": "RELIANCERELEATEDLISTEDCOMPANY",
      "exch_name": "O",
      "ubo_appl": "N",
      "ubo_count": "0",
      "ubo_name": " ",
      "ubo_pan": " ",
      "ubo_nation": " ",
      "ubo_add1": " ",
      "ubo_add2": " ",
      "ubo_add3": " ",
      "ubo_city": " ",
      "ubo_pin": " ",
      "ubo_state": " ",
      "ubo_cntry": " ",
      "ubo_add_ty": " ",
      "ubo_ctr": " ",
      "ubo_tin": " ",
      "ubo_id_ty": " ",
      "ubo_cob": " ",
      "ubo_dob": " ",
      "ubo_gender": " ",
      "ubo_fr_nam": " ",
      "ubo_occ": " ",
      "ubo_occ_ty": " ",
      "ubo_tel": " ",
      "ubo_mobile": " ",
      "ubo_code": " ",
      "ubo_hol_pc": "0",
      "sdf_flag": "Y",
      "ubo_df": " ",
      "aadhaar_rp": "123456789012",
      "new_change": "N",
      "log_name": " ",
      "filler1": "FILTERONE",
      "filler2": "FILTERTWO",
      "camsuploadstatus": "NOT UPLOADED",
      "camsresponsestatus": "PENDING",
      "camsremarks": " ",
      "kfinuploadstatus": "NOT UPLOADED",
      "kfinresponsestatus": "PENDING",
      "kfinremarks": " ",
      "memberid": "4292",
      "filename": "Fatca_Bulk_upload_individual.csv",
      "creatorid": "admin",
      "createddatetime": "07/10/2024 02:55:01 PM",
      "modifiedby": " ",
      "modifiedat": " "
    }
  ]
}
```

---

## 43. AOF Image Upload Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/AOF_IMAGE_UPLOAD_REPORT`  

PDF page: 139

**Sample Request Json**

```json
{
  "client_code": "500231",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "reporteLOG Upload Report _data_total": "2",
  "report_data": [
    {
      "date": "18/01/2025",
      "member_code": "04292",
      "client_code": "500233",
      "applicant_name": "NONDEMAT SONAL TEST",
      "tax_status": "INDIVIDUAL",
      "mode_of_holding": "JO",
      "document_type": "NRM",
      "pan": "DDDPD1234D",
      "pan_type": "F",
      "time_of_upload": "11:58 AM",
      "cams_status": "Uploaded - Ready to invest",
      "cams_reason": " ",
      "cams_response_upload_date": " ",
      "kfin_status": "Uploaded - Ready to invest",
      "kfin_reason": " ",
      "kfin_response_upload_date": " ",
      "created_at": "18/01/2025 11:58 AM"
    },
    {
      "date": "18/01/2025",
      "member_code": "04292",
      "client_code": "500233",
      "applicant_name": "NONDEMAT ASHOK TEST",
      "tax_status": "INDIVIDUAL",
      "mode_of_holding": "JO",
      "document_type": "NRM",
      "pan": "EEEPE1234E",
      "pan_type": "S",
      "time_of_upload": "11:58 AM",
      "cams_status": "Uploaded - Ready to invest",
      "cams_reason": " ",
      "cams_response_upload_date": " ",
      "kfin_status": "Uploaded - Ready to invest",
      "kfin_reason": " ",
      "kfin_response_upload_date": " ",
      "created_at": "18/01/2025 11:58 AM"
    }
  ]
}
```

---

## 44. eLOG Upload Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/ELOG_UPLOAD_REPORT`  

PDF page: 141

**Sample Request Json**

```json
{
  "client_code": "500231",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "2",
  "report_data": [
    {
      "date": "18/01/2025",
      "member_code": "04292",
      "client_code": "500233",
      "applicant_name": "NONDEMAT SONAL TEST",
      "tax_status": "INDIVIDUAL",
      "mode_of_holding": "JO",
      "elog_type": "NSELM",
      "pan": "DDDPD1234D",
      "pan_type": "F",
      "time_of_upload": "11:58 AM",
      "cams_status": "Uploaded - Ready to invest",
      "cams_reason": " ",
      "cams_response_upload_date": " ",
      "kfin_status": "Uploaded - Ready to invest",
      "kfin_reason": " ",
      "kfin_response_upload_date": " ",
      "created_at": "18/01/2025 11:58 AM"
    },
    {
      "date": "18/01/2025",
      "member_code": "04292",
      "client_code": "500233",
      "applicant_name": "NONDEMAT ASHOK TEST",
      "tax_status": "INDIVIDUAL",
      "mode_of_holding": "JO",
      "elog_type": "NSELM",
      "pan": "EEEPE1234E",
      "pan_type": "S",
      "time_of_upload": "11:58 AM",
      "cams_status": "Uploaded - Ready to invest",
      "cams_reason": " ",
      "cams_response_upload_date": " ",
      "kfin_status": "Uploaded - Ready to invest",
      "kfin_reason": " ",
      "kfin_response_upload_date": " ",
      "created_at": "18/01/2025 11:58 AM"
    }
  ]
}
```

---

## 45. SIP Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SIP_REG_REPORT`  

PDF page: 143

**Sample Request Json**

```json
{
  "sip_reg_id": "202503281000001",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "reportXSIP Registration Report _data_total": "1",
  "report_data": [
    {
      "status": "ACTIVE",
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "pg_bank_ref_no": "S7967212",
      "sip_reg_number": "202503281000001",
      "sip_reg_date": "28 MAR 2025",
      "amc_name": "AXIS MUTUAL FUND",
      "rta_scheme_code": "IOGP",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "frequency_type": "MONTHLY",
      "start_date": "28 APR 2025",
      "end_date": "27 APR 2026",
      "installments_amount": "2000",
      "entry_by": "SYSTEM",
      "dpc_flag": "Y",
      "dp_trans": "D",
      "first_order_today": "N",
      "sub_broker_code": "112256",
      "euin": "E989998",
      "euin_declaration": "Y",
      "folio_number": " ",
      "remarks": "TOP UP SIP REGISTRATION NO.61151",
      "sub_broker_arn_code": "ARN-66889",
      "no_of_installments": "12",
      "exchange_remark": " ",
      "health_declaration_flag": " ",
      "nominee_dob": " ",
      "disclaimer_flag": " ",
      "internal_ref_no": " ",
      "primary_holder_email": " ",
      "primary_holder_mobile": " ",
      "second_holder_email": "xyz@gmail.com",
      "second_holder_mobile": "9823456724",
      "third_holder_email": "xyz@gmail.com",
      "third_holder_mobile": "9823456724",
      "member_unique_id": "MUSIP0001"
    }
  ]
}
```

---

## 46. SIP Cancellation Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SIP_CAN_REPORT`  

PDF page: 145

**Sample Request Json**

```json
{
  "sip_reg_id": "202412231000078",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "internal_ref_num": " ",
      "sip_registration_no": "202412231000078",
      "sip_registration_date": "12/23/2024 04:27:00 PM",
      "sip_cancellation_date": "03/10/2025 09:00:05 PM",
      "amc_name": "ADITYA BIRLA MUTUAL FUND",
      "scheme_code": "BS41A-DP",
      "scheme_name": "ADITYA BIRLA SUN LIFE EQUITY SAVINGS FUND - DIVPAYOUT",
      "frequency_type": "MONTHLY",
      "start_date": "12/24/2024 12:00:00 AM",
      "end_date": "11/23/2028 12:00:00 AM",
      "next_due_date": "03/24/2025 12:00:00 AM",
      "no_of_installments_paid": "4",
      "installments_amt": "1000",
      "total_installment_amt_paid": "4000",
      "cancelled_by": " ",
      "sip_status": "CXL",
      "remark": "SIP CANCELED DUE TO THREE CONSECUTIVE INVALID INSTALLMENTS"
    }
  ]
}
```

---

## 47. SIP Installment Due Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SIP_INST_DUE_REPORT`  

PDF page: 146

**Sample Request Json**

```json
{
  "sip_reg_id": "202412071000017",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "internal_ref_no": " ",
      "sip_reg_number": "202412071000017",
      "reg_date": "07 DEC 2024",
      "amc_name": "AXIS MUTUAL FUND",
      "scheme_code": "AXMCGP-GR",
      "scheme_name": "AXIS MID CAP FUND - GROWTH",
      "frequency_type": "MONTHLY",
      "installment_amt": "1000",
      "due_date": "01 APR 2025",
      "prev_paid_date": "03 MAR 2025",
      "no_of_installments_paid": "1",
      "total_installment_amt_paid": "1000",
      "entry_by": "SYSTEM",
      "dp_trans": "D",
      "first_order_today": "N"
    }
  ]
}
```

---

## 48. SIP Topup Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SIP_TOPUP_REPORT`  

PDF page: 148

**Sample Request Json**

```json
{
  "parent_sip_reg_id": "202503031000007",
  "client_code": "NDNTUCC77",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "NDNTUCC77",
      "client_name": "PARIXIT G PATEL",
      "reg_no": "61377",
      "scheme_code": "IOGP",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "sip_xsip_amount": "10000",
      "start_date": "07-Mar-2025",
      "end_date": "07-Feb-2026",
      "top_up_amount": "500",
      "date_of_activation": "03-Mar-2025",
      "entry_by": "ADMIN",
      "principle_sip_reg_no": "202503031000007",
      "principle_sip_internal_ref_no": "S8467231",
      "last_child_sip_reg_no": "202503031000010",
      "top_up_frequency": "ANNUALLY",
      "top_up_status": "ACTIVE"
    }
  ]
}
```

---

## 49. Stepup Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/STEPUP_REG_REPORT`  

PDF page: 149

**Sample Request Json**

```json
{
  "sip_reg_id": "202503031000024",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "status": "ACTIVE",
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "sip_xsip_regn_number": "202503031000024",
      "sip_xsip_regn_date": "03 MAR 2025",
      "sip_xsip_type": "SIP",
      "amc_name": "ADITYA BIRLA MUTUAL FUND",
      "rta_scheme_code": "ABSL",
      "scheme_code": "ABCTX-GR",
      "scheme_name": "ADITYA TAX SAVING FUND - DIRECT PLAN GR",
      "frequency_type": "MONTHLY",
      "start_date": "07 FEB 2025",
      "end_date": "06 FEB 2035",
      "stepup_start__effective_date": "07 MAR 2025",
      "stepup_enddate": "07 FEB 2027",
      "stepup_frequency": "ANNUAL",
      "stepup_amount": "500",
      "entry_by": "ADMIN"
    }
  ]
}
```

---

## 50. XSIP Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/XSIP_REG_REPORT`  

PDF page: 151

**Sample Request Json**

```json
{
  "xsip_reg_id": "202503281000001",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "status": "CXL",
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "pg_bank_ref_no": "BANKREF123",
      "xsip_registration_no": "202503131000001",
      "xsip_registration_date": "13 MAR 2025",
      "amc_name": "AXIS MUTUAL FUND",
      "rta_scheme_code": "IOGP",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "frequency_type": "DAILY",
      "start_date": "13 MAR 2025",
      "end_date": "15 FEB 2035",
      "installments_amount": "10000",
      "brokerage": "0",
      "entry_by": "ADMIN",
      "nse_mandate_id": "2023072810001",
      "dpc_flag": "Y",
      "dp_trans": "D",
      "sub_broker": "112256",
      "euin_no": "E989998",
      "euin_declaration": "Y",
      "first_order_today": "N",
      "folio_number": " ",
      "remarks": "XSIP DATA 3221",
      "sub_broker_arn": "ARN-66889",
      "no_of_installments": "2586",
      "exchange_remark": " ",
      "health_declaration_flag": " ",
      "nominee_dob": " ",
      "disclaimer_flag": " ",
      "internal_ref_no": " ",
      "primary_holder_email": "PARIXIT.PATEL@NJGROUP.IN",
      "primary_holder_mobile": "9898573329",
      "second_holder_email": "xyz@gmail.com",
      "second_holder_mobile": "9823456724",
      "third_holder_email": "xyz@gmail.com",
      "third_holder_mobile": "9823456724",
      "member_unique_id": "MUXSIP0001"
    }
  ]
}
```

---

## 51. XSIP Cancellation Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/XSIP_CAN_REPORT`  

PDF page: 153

**Sample Request Json**

```json
{
  "xsip_reg_id": "202503281000001",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "status": "CXL",
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "internal_ref_num": "BANKREF123",
      "xsip_registration_no": "202503131000001",
      "xsip_registration_date": "13/03/2025",
      "xsip_cancellation_date": "21/03/2025",
      "amc_name": "AXIS MUTUAL FUND",
      "scheme_code": "AXIOGP-GR",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "frequency_type": "DAILY",
      "start_date": "13/03/2025",
      "end_date": "15/02/2035",
      "next_due_date": " ",
      "no_of_installments_paid": "5",
      "installments_amt": "10000",
      "brokerage": "0",
      "total_installment_amt_paid": "50000",
      "cancelled_by": " ",
      "nse_mandate_id": "2023072810001",
      "remark": "SIP CANCELED DUE TO THREE CONSECUTIVE INVALID INSTALLMENTS"
    }
  ]
}
```

---

## 52. XSIP Installment Due Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/XSIP_INST_DUE_REPORT`  

PDF page: 154

**Sample Request Json**

```json
{
  "xsip_reg_id": "202503281000001",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "internal_ref_no": " ",
      "sip_reg_number": "202412311000001",
      "reg_date": "31 Dec 2024",
      "amc_name": "AXIS MUTUAL FUND",
      "scheme_code": "AXMCGP-GR",
      "scheme_name": "AXIS MID CAP FUND - GROWTH",
      "frequency_type": "MONTHLY",
      "installment_amt": "1000",
      "due_date": "01 Apr 2025",
      "prev_paid_date": "03 Mar 2025",
      "no_of_installments_paid": "2",
      "total_installment_amt_paid": "2000",
      "entry_by": "SYSTEM",
      "mandate_id": "2023072810001",
      "dp_trans": "D",
      "first_order_today": "N"
    }
  ]
}
```

---

## 53. XSIP Topup Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/XSIP_TOPUP_REPORT`  

PDF page: 156

**Sample Request Json**

```json
{
  "parent_xsip_reg_id": "202501221000001",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "reg_no": "61371",
      "scheme_code": "MCGP",
      "scheme_name": "AXIS MID CAP FUND - GROWTH",
      "sip_xsip_amount": "1000.00",
      "start_date": "28-Feb-2025",
      "end_date": "28-Jan-2027",
      "top_up_amount": "1000.00",
      "date_of_activation": "22-Jan-2025",
      "entry_by": "ADMIN",
      "principle_sip_reg_no": "202501221000001",
      "principle_sip_internal_ref_no": "S8467231",
      "last_child_sip_reg_no": "202501311000001",
      "top_up_frequency": "ANNUALLY",
      "top_up_status": "ACTIVE"
    }
  ]
}
```

---

## 54. STP Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/STP_REG_REPORT`  

PDF page: 157

**Sample Request Json**

```json
{
  "stp_reg_id": "202503131000015",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "status": "ACTIVE",
      "member_code": "12345",
      "client_code": "5100004",
      "stp_registration_no": "202503131000015",
      "folio_no": " ",
      "internal_ref_no": " ",
      "from_amc_name": "AXIS MUTUAL FUND",
      "to_amc_name": "AXIS MUTUAL FUND",
      "from_scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "to_scheme_name": "AXIS GILT FUND - HALF YEARLY DIVIDEND REINVESTMENT",
      "stp_registration_date": "13 MAR 2025",
      "stp_start_date": "31 MAR 2025",
      "stp_end_date": "18 JUL 2027",
      "frequency_type": "FORTNIGHTLY",
      "trxn_mode": "DEMAT",
      "transfer_amount": "0",
      "transfer_units": "10",
      "no_of_transfers": "60",
      "first_order_todays_flag": "N",
      "euin_declaration": "Y",
      "euin_number": "E554354",
      "sub_br_code": "112256",
      "remarks": " ",
      "sub_br_arn_code": "ARN-66889",
      "buy_sell_type": "ADDITIONAL",
      "from_nse_scheme_code": "AXIOGP-GR",
      "to_nse_scheme_code": "AXCMHD-DR",
      "email_id": " ",
      "mobile_no": " ",
      "member_unique_id": "MUSTP0001"
    }
  ]
}
```

---

## 55. STP Cancellation Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/STP_CAN_REPORT`  

PDF page: 159

**Sample Request Json**

```json
{
  "stp_reg_id": "202308021000016",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "stp_registration_no": "202308021000016",
      "folio_no": " ",
      "from_amc_name": "AXIS MUTUAL FUND",
      "to_amc_name": "AXIS MUTUAL FUND",
      "from_scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "to_scheme_name": "AXIS GILT FUND - HALF YEARLY DIVIDEND REINVESTMENT",
      "stp_registration_date": "02 AUG 2023",
      "stp_start_date": "10 AUG 2023",
      "stp_end_date": "10 JUL 2024",
      "frequency": "MONTHLY",
      "trxn_mode": "DEMAT",
      "transfer_amount": "0",
      "transfer_units": "10",
      "no_of_transfers": "12",
      "euin_declaration": "Y",
      "euin_number": "E989998",
      "sub_br_code": "112256",
      "remarks": " ",
      "stp_cancellation_date": "02 AUG 2023",
      "stp_cancelled_by": "ADMIN"
    }
  ]
}
```

---

## 56. STP Installment Due Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/STP_INST_DUE_REPORT`  

PDF page: 161

**Sample Request Json**

```json
{
  "stp_reg_id": "202405291000014",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "stp_registration_no": "202405291000014",
      "client_name": "165024-YUG P PATEL",
      "folio_no": "12345678912345678903",
      "internal_ref_no": "STP374698",
      "stp_registration_date": "29/05/2024 17:08:22",
      "amc_name": "AXIS MUTUAL FUND",
      "from_scheme_name": "AXCMHD-DR-AXIS GILT FUND - HALF YEARLY DIVIDENDREINVESTMENT",
      "to_scheme_name": "AXMCGP-GR-AXIS MID CAP FUND - GROWTH",
      "frequency_type": "MONTHLY",
      "dp_trans": "P",
      "transfer_amount": "0",
      "transfer_units": "333",
      "due_date": "05 APR 2025",
      "prev_transfer_date": "05 MAR 2025",
      "no_of_transfer_completed": "10",
      "first_order_todays_flag": "N",
      "euin_declaration": "Y",
      "euin_number": "E479425",
      "sub_br_code": "24542",
      "remarks": " ",
      "entry_by": "ADMIN"
    }
  ]
}
```

---

## 57. SWP Registration Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SWP_REG_REPORT`  

PDF page: 163

**Sample Request Json**

```json
{
  "swp_reg_id": "202503181000006",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025",
  "member_unique_ids": ""
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "status": "ACTIVE",
      "member_code": "12345",
      "client_code": "5100004",
      "swp_registration_no": "202503181000006",
      "folio_no": " ",
      "amc": "AXIS MUTUAL FUND",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "frequency_type": "DAILY",
      "swp_registration_date": "18 Mar 2025",
      "swp_start_date": "21 Mar 2025",
      "swp_end_date": "21 Feb 2030",
      "withdrawl_amount": "0",
      "withdrawal_units": "1",
      "no_of_withdrawls": "1283",
      "euin_declaration": "Y",
      "euin_number": "E554354",
      "subbrcode": "112256",
      "first_order_flag": "Y",
      "int_ref_no": " ",
      "remark": " ",
      "sub_broker_arn_code": "ARN-66889",
      "nse_scheme_code": "AXIOGP-GR",
      "transaction_mode": "DEMAT",
      "mobile_no": " ",
      "email_id": " ",
      "bank_account_no": "3112426522",
      "member_unique_id": "MUSWP0001"
    }
  ]
}
```

---

## 58. SWP Cancellation Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SWP_CAN_REPORT`  

PDF page: 165

**Sample Request Json**

```json
{
  "swp_reg_id": "202308011050080",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "swp_registration_no": "202308011050080",
      "folio_no": " ",
      "amc": "AXIS MUTUAL FUND",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "swp_registration_date": "01 Aug 2023",
      "swp_cancellation_date": "01 Aug 2023 17:53:21",
      "swp_start_date": "01 Sep 2023",
      "swp_end_date": "01 Jul 2024",
      "frequency_type": "MONTHLY",
      "withdrawl_amount": "0",
      "withdrawl_units": "10",
      "no_of_withdrawls": "12",
      "euin_declaration": "Y",
      "euin_number": "E989998",
      "subbrcode": "112256",
      "remark": " ",
      "swp_cancelled_by": "ADMIN",
      "nse_scheme_code": "AXIOGP-GR"
    }
  ]
}
```

---

## 59. SWP Installment Due Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SWP_INST_DUE_REPORT`  

PDF page: 166

**Sample Request Json**

```json
{
  "swp_reg_id": "202412271000003",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "5100004",
      "client_name": "Krushnakant Bharatbhai Desai",
      "swp_regn_no": "202412271000003",
      "folio_no": " ",
      "internal_ref_no": "SWP12346",
      "regn_date": "27/12/2024 12:09:28",
      "amc_name": "AXIS MUTUAL FUND",
      "scheme_code": "AXMCGP-GR",
      "scheme_name": "AXIS MID CAP FUND - GROWTH",
      "frequency_type": "MONTHLY",
      "installment_amt": "0",
      "installment_units": "10",
      "due_date": "01 APR 2025",
      "prev_paid_date": "03 MAR 2025",
      "no_of_installments_paid": "3",
      "total_installment_amt_sold": "0",
      "unit_sold": "30",
      "entry_by": "ADMIN",
      "dp_trans": "D",
      "euin_declaration": "Y",
      "euin_number": "E989998",
      "subbrcode": "112256",
      "first_order_flag": "N",
      "remark": " "
    }
  ]
}
```

---

## 60. Scheme Master, NAV & Settlement calendar Download API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/MASTER_DOWNLOAD`  

PDF page: 168

> Note: Request is JSON, but a successful response is NOT JSON: a pipe (|) separated .txt file is downloaded (names: NSE_NSEINVEST_ALL / SIP / STP / SWP / NAV / SET _<DDMMYYYY>.txt; NAV file has no header). On failure you get: `{"response_status":"F","response_status_remarks":"No Record Found!!"}`.

**Sample Request Json**

```json
{
  "file_type": "SCH"
}
```

---

## 61. Client KYC Status Report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/CLIENT_KYC_REPORT`  

PDF page: 169

**Sample Request Json**

```json
{
  "pan_no": "BVYPD3824K",
  "client_code": "5100004",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "client_code": "",
      "client_pan": "",
      "holding_type": "",
      "holder_name": "",
      "holder_dob": "",
      "kyc_status": "",
      "status_remark": ""
    }
  ]
}
```

---

## 62. KYC FRESH REGISTER API

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/EKYC/EKYCREG`  

PDF page: 170

**Sample Request Json**

```json
{
  "amcCode": "AXF",
  "panNo": "BVYPD3824K",
  "mobileNo": "9748975934",
  "invEmail": "abc@gmail.com"
}
```

Doc comments: Doc prints an extra '{' and leading spaces inside keys/values; normalized here.

**Sample Response Json**

```json
{
  "link": "https://nseinvestuat.nseindia.com/nsemfdesk/ekycVerifyByUser/3A2FE45B4015ECDDE06332C911AC3C1F",
  "message": "EKYC FRESH REGISTRATION REQUEST RECEVIED"
}
```

---

## 63. Purchase orders payment API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/payments/purchase_payment`  

PDF page: 171

> Note: Request body differs per payment_mode (MANDATE, CHEQUE, UPI, NETBANKING, NEFT/RTGS). Response samples in the doc contain inline comments and typos that were cleaned here.

**Sample Request Json: MANDATE**

```json
{
  "payment_mode": "MANDATE",
  "client_code": "K0281",
  "order_ids": "451200000005,451200000012,451190000015",
  "mandate_id": "2025050100001"
}
```

**Sample Response Json: MANDATE**

```json
{
  "payment_mode": "MANDATE",
  "client_code": "K0281",
  "order_ids": "451200000005",
  "mandate_id": "2025050100001",
  "status": "success",
  "order_amount": 5000,
  "remark": "successfully done.",
  "short_url": "https://nseinvest.com/mf/abcdef01",
  "basket_id": "451200000005"
}
```

Doc comments: or fail message; success or fail; total order amount

**Sample Request Json: CHEQUE**

```json
{
  "payment_mode": "CHEQUE",
  "client_code": "K0281",
  "order_ids": "451200000005",
  "bank_account_no": "1234567890",
  "ifsc": "KKBK0000123",
  "cheque_no": "512",
  "cheque_date": "01/05/2025"
}
```

**Sample Response Json: CHEQUE**

```json
{
  "payment_mode": "CHEQUE",
  "client_code": "K0281",
  "order_ids": "451200000005 ",
  "bank_account_no": "1234567890",
  "ifsc": "KKBK0000123",
  "cheque_no": "512",
  "cheque_date": "01-05-2025",
  "status": "success",
  "order_amount": "5000",
  "remark": "successfully done.",
  "short_url": "https://nseinvest.com/mf/abcdef01",
  "basket_id": "451200000005"
}
```

Doc comments: or fail message; success or fail

**Sample Request Json: UPI**

```json
{
  "payment_mode": "UPI",
  "client_code": "K0281",
  "order_ids": "451200000005",
  "bank_account_no": "1234567890",
  "ifsc": "KKBK0000123",
  "vpa": " krushnakant@upi ",
  "callback_url": "https://member-site.com/upi-callback"
}
```

**Sample Response Json: UPI**

```json
{
  "payment_mode": "UPI",
  "client_code": "NDI65",
  "order_ids": "461490000306",
  "bank_account_no": "125632541841500",
  "ifsc": "HDFC0000060",
  "vpa": "krushnakant@upi",
  "callback_url": "https://member-site.com/upi-callback",
  "status": "success",
  "order_amount": "100",
  "remark": "successfully done",
  "short_url": "https://nseinvestuat.nseindia.com/nsemfclient/trxnpaymentonline/52EE2171CBCC9070E06332C911ACB01F",
  "basket_id": "461490000306"
}
```

**Sample Request Json: NETBANKING**

```json
{
  "payment_mode": "NETBANKING",
  "client_code": "K0281",
  "order_ids": "451200000005,451200000012,451190000015",
  "bank_account_no": "1234567890",
  "ifsc": "KKBK0000123",
  "callback_url": "https://member-site.com/nb-callback"
}
```

**Sample Response Json: NETBANKING**

```json
{
  "payment_mode": "NETBANKING",
  "client_code": "K0281",
  "order_ids": "451200000005",
  "bank_account_no": "1234567890",
  "ifsc": "KKBK0000123",
  "callback_url": "https://member-site.com/nb-callback",
  "status": "success",
  "order_amount": 5000,
  "remark": "successfully done.",
  "short_url": "https://nseinvest.com/mf/abcdef01",
  "basket_id": "451200000005"
}
```

Doc comments: or fail message; success or fail

**Sample Request Json: NEFT/RTGS**

```json
{
  "payment_mode": "NEFT",
  "client_code": "K0281",
  "order_ids": "451200000005",
  "neft_rtgs_utr_no": "123456789"
}
```

**Sample Response Json: NEFT/RTGS**

```json
{
  "payment_mode": "NEFT",
  "client_code": "K0281",
  "order_ids": "451200000005",
  "status": "success",
  "order_amount": 5000,
  "remark": "successfully done.",
  "short_url": "https://nseinvest.com/mf/abcdef01",
  "neft_rtgs_utr_no": " 123456789",
  "basket_id": "451200000005"
}
```

Doc comments: or fail message; success or fail

---

## 64. UPI payment status check API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/payments/upi_status_check`  

PDF page: 175

> Note: The same response JSON is also POSTed to your `callback_url` on success or failure.

**Sample Request Json**

```json
{
  "nse_upi_ref_no": "123",
  "client_code": "K0281"
}
```

**Sample Response Json and POST on callback_url (on success or fail)**

```json
{
  "payment_mode": "UPI",
  "client_code": "K0281",
  "bank_account_no": "1234567890",
  "ifsc": "KKBK0000123",
  "vpa": "krushnakant@upi",
  "status": "SUCCESS",
  "order_amount": 5000,
  "remark": "Transaction success",
  "nse_upi_ref_no": "123",
  "upi_tran_ref_id": "1234567",
  "cust_ref_no": "123456789012"
}
```

Doc comments: 12 digit Retrieval Reference Number (RRN); Unique UPI Transaction ID; or fail message; values: SUCCESS, FAILED, PENDING, EXPIRED, REJECTED

---

## 65. SWP Cancellation Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/cancellation/SWP_CAN`  

PDF page: 176

**Sample Request Json**

```json
{
  "can_data": [
    {
      "client_code": "1001",
      "swp_reg_no": "1747",
      "remarks": "SWP cancel 1747"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "reg_data": [
    {
      "client_code": "1001",
      "swp_reg_no": "1747",
      "remarks": "SWP CANCEL 1747",
      "can_status": "CAN_FAILED",
      "can_remark": "Invalid SWP registration number"
    }
  ]
}
```

---

## 66. SIP/XSIP Pause Service API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/XSIP_PAUSE`  

PDF page: 177

**Sample Request Json**

```json
{
  "pause_data": [
    {
      "sip_reg_no": "202505011000001",
      "effective_date": "15/05/2025",
      "pause_flag": "Y",
      "remarks": "requested by investor"
    }
  ]
}
```

**Sample Response Json**

```json
{
  "pause_data": [
    {
      "sip_reg_no": "202505011000001",
      "effective_date": "15/05/2025",
      "pause_flag": "Y",
      "remarks": "requested by investor",
      "pause_status": "SUCCESS",
      "pause_remark": "xsip pause successfully"
    }
  ]
}
```

Doc comments: values SUCCESS, FAILED

---

## 67. Client Master report API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/client_master_report`  

PDF page: 178

**Sample Request Json**

```json
{
  "client_code": "K123",
  "PAN": "BVYPED3824K",
  "from_date": "21-01-2025",
  "to_date": "28-01-2025"
}
```

**Sample Response Json**

```json
{
  "response_status": "S",
  "report_data_total": "1",
  "report_data": [
    {
      "member_code": "12345",
      "client_code": "109780",
      "primary_holder_first_name": "PARIXIT",
      "primary_holder_middle_name": "GIRISHBHAI",
      "primary_holder_last_name": "PATEL",
      "tax_status": "INDIVIDUAL",
      "gender": "MALE",
      "primary_holder_dob_incorporation": "01/01/1990",
      "occupation_code": "BUSINESS",
      "holding_nature": "JOINT",
      "second_holder_first_name": "SECOND",
      "second_holder_middle_name": "MIDDLE",
      "second_holder_last_name": "LAST",
      "third_holder_first_name": "THIRD",
      "third_holder_middle_name": "MIDDLE",
      "third_holder_last_name": "LAST",
      "second_holder_dob": "01/01/1991",
      "third_holder_dob": "01/01/1992",
      "guardian_first_name": " ",
      "guardian_middle_name": " ",
      "guardian_last_name": " ",
      "guardian_dob": " ",
      "primary_holder_pan_exempt": "NO",
      "second_holder_pan_exempt": "NO",
      "third_holder_pan_exempt": "NO",
      "guardian_pan_exempt": " ",
      "primary_holder_pan": "DHQPK6568F",
      "second_holder_pan": "DHQPK6568A",
      "third_holder_pan": "DHQPK6568B",
      "guardian_pan": " ",
      "primary_holder-exempt_category": " ",
      "second_holder_exempt_category": " ",
      "third_holder_exempt_category": " ",
      "guardian_exempt_category": " ",
      "client_type": "DEMAT",
      "dp_status": "ACTIVE",
      "dp_status_remarks": " ",
      "pms": "NO",
      "default_dp": "CDSL",
      "cdsl_dpid": "12064200",
      "cdslcltid": "1206420012345123",
      "cmbp_id": "12345666",
      "nsdldpid": " ",
      "nsdlcltid": " ",
      "account_type_1": "CB",
      "account_no_1": "7857867862",
      "micr_no_1": " ",
      "ifsc_code_1": "SBIN0000018",
      "bank_name_1": "STATE BANK OF INDIA",
      "bank_branch_1": "BALLYGUNGE",
      "default_bank_flag_1": "NO",
      "bank1_created_at": "16/04/2025 02:58:56 PM",
      "bank1_last_modified_at": "16/04/2025 02:58:56 PM",
      "bank1_status": "PENDING",
      "bank1_status_remarks": " ",
      "account_type_2": "SB",
      "account_no_2": "5235562356",
      "micr_no_2": " ",
      "ifsc_code_2": "SBIN0000018",
      "bank_name_2": "STATE BANK OF INDIA",
      "bank_branch_2": "BALLYGUNGE",
      "default_bank_flag_2": "YES",
      "bank2_created_at": "16/04/2025 02:58:56 PM",
      "bank2_last_modified_at": "16/04/2025 02:58:56 PM",
      "bank2_status": "PENDING",
      "bank2_status_remarks": " ",
      "account_type_3": " ",
      "account_no_3": " ",
      "micr_no_3": " ",
      "ifsc_code_3": " ",
      "bank_name_3": " ",
      "bank_branch_3": " ",
      "default_bank_flag_3": " ",
      "bank3_created_at": " ",
      "bank3_last_modified_at": " ",
      "bank3_status": " ",
      "bank3_status_remarks": " ",
      "account_type_4": " ",
      "account_no_4": " ",
      "micr_no_4": " ",
      "ifsc_code_4": " ",
      "bank_name_4": " ",
      "bank_branch_4": " ",
      "default_bank_flag_4": " ",
      "bank4_created_at": " ",
      "bank4_last_modified_at": " ",
      "bank4_status": " ",
      "bank4_status_remarks": " ",
      "account_type_5": " ",
      "account_no_5": " ",
      "micr_no_5": " ",
      "ifsc_code_5": " ",
      "bank_name_5": " ",
      "bank_branch_5": " ",
      "default_bank_flag_5": " ",
      "bank5_created_at": " ",
      "bank5_last_modified_at": " ",
      "bank5_status": " ",
      "bank5_status_remarks": " ",
      "cheque_name": "MY CHEQUE NAMETEST",
      "div_pay_mode": "01",
      "address_1": "ADDRESS_1",
      "address_2": "ADDRESS_2",
      "address_3": "ADDRESS_3",
      "city": "MUMBAI",
      "state": "MAHARASHTRA",
      "pincode": "400008",
      "country": "INDIA",
      "resi._phone": "123123123",
      "resi._fax": "321321321",
      "office_phone": "789789789",
      "office_fax": "987987987",
      "email": "ABC@XYZ.COM",
      "communication_mode": "ELECTRONIC",
      "foreign_address_1": " ",
      "foreign_address_2": " ",
      "foreign_address_3": " ",
      "foreign_address_city": " ",
      "foreign_address_pincode": " ",
      "foreign_address_state": " ",
      "foreign_address_country": " ",
      "foreign_address_resi_phone": " ",
      "foreign_address_fax": " ",
      "foreign_address_off._phone": " ",
      "foreign_address_off._fax": " ",
      "indian_mobile_no.": "9714849771",
      "primary_holder_kyc_type": "CKYC COMPLIANT",
      "primary_holder_ckyc_number": "1234567891",
      "second_holder_kyc_type": "CKYC COMPLIANT",
      "second_holder_ckyc_number": "213343545",
      "third_holder_kyc_type": "CKYC COMPLIANT",
      "third_holder_ckyc_number": "455465765765",
      "guardian_kyc_type": " ",
      "guardian_ckyc_number": " ",
      "primary_holder_kra_exempt_ref._no.": " ",
      "second_holder_kra_exempt_ref._no.": " ",
      "third_holder_kra_exempt_ref._no": " ",
      "guardian_exempt_ref._no": " ",
      "aadhaar_updated": "YES",
      "mapin_id.": "1234527887654321",
      "paperless_flag": "Paper",
      "lei_no": "98787656445345678909",
      "lei_validity": "01/01/2027",
      "email_declaration_flag": "Self",
      "mobile_declaration_flag": "Self",
      "second_holder_email": "SECOND@GMAIL.COM",
      "second_holder_email_declaration": "Self",
      "second_holder_mobile": "9878987678",
      "second_holder_mobile_declaration": "Self",
      "third_holder_email": "THIRD@GMAIL.COM",
      "third_holder_email_declaration": "Self",
      "third_holder_mobile": "9876456789",
      "third_holder_mobile_declaration": "Self",
      "guardian_relationship": " ",
      "nomination_opt": "Y",
      "nomination_authentication_mode": "OTP",
      "nominee_1_name": "NOMINEE1NAME",
      "nominee_1_relationship": "AUNT",
      "nominee_1_applicable": "50",
      "nominee_1_minor_flag": "NO",
      "nominee_1_dob": " ",
      "nominee_1_guardian": " ",
      "nominee_1_guardian_pan": " ",
      "nominee_1_identity_type": "",
      "nominee_1_id_number": "",
      "nominee_1_email": "",
      "nominee_1_mobile": "",
      "nominee_1_address1": "",
      "nominee_1_address2": "",
      "nominee_1_address3": "",
      "nominee_1_city": "",
      "nominee_1_pin": "",
      "nominee_1_country": "",
      "nominee_2_name": "NOMINNE2",
      "nominee_2_relationship": "BROTHER-IN-LAW",
      "nominee_2_applicable": "30",
      "nominee_2_dob": "01/01/2015",
      "nominee_2_minor_flag": "YES",
      "nominee_2_guardian": "NOMINEEGUAR",
      "nominee_2_guardian_pan": "EFROP0987T",
      "nominee_2_identity_type": "",
      "nominee_2_id_number": "",
      "nominee_2_email": "",
      "nominee_2_mobile": "",
      "nominee_2_address1": "",
      "nominee_2_address2": "",
      "nominee_2_address3": "",
      "nominee_2_city": "",
      "nominee_2_pin": "",
      "nominee_2_country": "",
      "nominee_3_name": "NOMM3",
      "nominee_3_relationship": "BROTHER",
      "nominee_3_applicable": "20",
      "nominee_3_dob": " ",
      "nominee_3_minor_flag": "NO",
      "nominee_3_guardian": " ",
      "nominee_3_guardian_pan": " ",
      "nominee_3_identity_type": "",
      "nominee_3_id_number": "",
      "nominee_3_email": "",
      "nominee_3_mobile": "",
      "nominee_3_address1": "",
      "nominee_3_address2": "",
      "nominee_3_address3": "",
      "nominee_3_city": "",
      "nominee_3_pin": "",
      "nominee_3_country": "",
      "nominee_names_registration_status_in_soa": "",
      "created_by": "ADMIN",
      "created_at": "16/04/2025 02:58:56 PM",
      "last_modified_by": " ",
      "last_modified_at": "30/04/2025 01:53:42 PM"
    }
  ],
  "error_remark": ""
}
```

---

## 68. Change API Secret

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/admin/CHANGE_API_SECRET`  

PDF page: 184

**Sample Request Json**

```json
{}
```

Doc comments: empty json request body

**Sample Response Json**

```json
{
  "api_secret": "39159877D689FE35E063250704120712"
}
```

---

## 69. Nominee Registration/modification

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/NOM`  

PDF page: 184

**Sample Request Json**

```json
{
  "nft_nominee_registration/modification_details ": [
    {
      "AMC_CODE ": "",
      "FOLIO_NO ": "",
      "NCT_TYPE ": "",
      "FH_NAME": "",
      "TAX_NUMBER ": "",
      "DOC_TYPE ": "",
      "TWOFA_AUTH ": "",
      "IMG_REF_NO ": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "NOM_OPT": "",
      "NOM1_NAME": "",
      "NOM1_RELA": "",
      "NOM1_PER ": "",
      "NOM1_IDNO": "",
      "NOM1_MIN_F ": "",
      "NOM1_DOB ": "",
      "NOM1_GUARD ": "",
      "NOM1_GRELA ": "",
      "NOM1_GPAN": "",
      "NOM2_NAME": "",
      "NOM2_RELA": "",
      "NOM2_PER ": "",
      "NOM2_IDNO": "",
      "NOM2_MIN_F ": "",
      "NOM2_DOB ": "",
      "NOM2_GUARD ": "",
      "NOM2_GRELA ": "",
      "NOM2_GPAN": "",
      "NOM3_NAME": "",
      "NOM3_RELA": "",
      "NOM3_PER ": "",
      "NOM3_IDNO": "",
      "NOM3_MIN_F ": "",
      "NOM3_DOB ": "",
      "NOM3_GUARD ": "",
      "NOM3_GRELA ": "",
      "NOM3_GPAN": "",
      "NOM_COUNT": "",
      "NOM_SOA": "",
      "NOM1_ID_T": "",
      "NOM2_ID_T": "",
      "NOM3_ID_T": "",
      "NOM1_EMAI": "",
      "NOM2_EMAI": "",
      "NOM3_EMAI": "",
      "NOM1_MOB ": "",
      "NOM2_MOB ": "",
      "NOM3_MOB ": "",
      "NOM1_ADD1": "",
      "NOM1_ADD2": "",
      "NOM1_ADD3": "",
      "NOM2_ADD1": "",
      "NOM2_ADD2": "",
      "NOM2_ADD3": "",
      "NOM3_ADD1": "",
      "NOM3_ADD2": "",
      "NOM3_ADD3": "",
      "NOM1_CITY": "",
      "NOM1_PIN ": "",
      "NOM1_CON ": "",
      "NOM2_CITY": "",
      "NOM2_PIN ": "",
      "NOM2_CON ": "",
      "NOM3_CITY": "",
      "NOM3_PIN ": "",
      "NOM3_CON ": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": "",
      "Filler_8": "",
      "Filler_9": "",
      "Filler_10": "",
      "Filler_11": "",
      "Filler_12": "",
      "Filler_13": "",
      "Filler_14": "",
      "Filler_15": "",
      "Filler_16": "",
      "Filler_17": "",
      "Filler_18": "",
      "Filler_19": "",
      "Filler_20": "",
      "Filler_21": "",
      "Filler_22": "",
      "Filler_23": "",
      "Filler_24": "",
      "Filler_25": "",
      "Filler_26": "",
      "Filler_27": "",
      "Filler_28": "",
      "Filler_29": "",
      "Filler_30": "",
      "Filler_31": "",
      "Filler_32": "",
      "Filler_33": "",
      "Filler_34": "",
      "Filler_35": "",
      "Filler_36": "",
      "Filler_37": "",
      "Filler_38": "",
      "Filler_39": "",
      "Filler_40": "",
      "Filler_41": "",
      "Filler_42": "",
      "Filler_43": "",
      "Filler_44": "",
      "Filler_45": "",
      "Filler_46": "",
      "Filler_47": "",
      "Filler_48": "",
      "Filler_49": "",
      "Filler_50": "",
      "Filler_51": "",
      "Filler_52": "",
      "Filler_53": "",
      "Filler_54": "",
      "Filler_55": "",
      "Filler_56": "",
      "Filler_57": "",
      "Filler_58": "",
      "Filler_59": "",
      "Filler_60": "",
      "Filler_61": "",
      "Filler_62": "",
      "Filler_63": "",
      "Filler_64": "",
      "Filler_65": "",
      "Filler_66": "",
      "Filler_67": "",
      "Filler_68": "",
      "Filler_69": "",
      "Filler_70": "",
      "Filler_71": "",
      "Filler_72": "",
      "Filler_73": "",
      "Filler_74": "",
      "Filler_75": "",
      "Filler_76": "",
      "Filler_77": "",
      "Filler_78": "",
      "Filler_79": "",
      "Filler_80": "",
      "Filler_81": "",
      "Filler_82": "",
      "Filler_83": "",
      "Filler_84": "",
      "Filler_85": "",
      "Filler_86": "",
      "Filler_87": "",
      "Filler_88": "",
      "Filler_89": "",
      "Filler_90": "",
      "Filler_91": "",
      "Filler_92": "",
      "Filler_93": "",
      "Filler_94": "",
      "Filler_95": "",
      "Filler_96": "",
      "Filler_97": "",
      "Filler_98": "",
      "Filler_99": "",
      "Filler_100": "",
      "Filler_101": "",
      "Filler_102": "",
      "Filler_103": "",
      "Filler_104": "",
      "Filler_105": "",
      "Filler_106": "",
      "Filler_107": "",
      "Filler_108": "",
      "Filler_109": "",
      "Filler_110": "",
      "Filler_111": "",
      "Filler_112": "",
      "Filler_113": "",
      "Filler_114": "",
      "Filler_115": "",
      "Filler_116": "",
      "Filler_117": "",
      "Filler_118": "",
      "Filler_119": "",
      "Filler_120": "",
      "Filler_121": "",
      "Filler_122": "",
      "Filler_123": "",
      "Filler_124": "",
      "Filler_125": "",
      "Filler_126": "",
      "Filler_127": "",
      "Filler_128": "",
      "Filler_129": "",
      "Filler_130": "",
      "Filler_131": "",
      "Filler_132": "",
      "Filler_133": "",
      "Filler_134": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "Message": "NFT - Change of Nominee record Added successfully.",
  "Status": "Success"
}
```

---

## 70. Change of Multiple Banks

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/COA`  

PDF page: 204

> Note: The doc gives the same endpoint (`/api/v1/NFT/COA`) for "Change of Multiple Banks" and "Change of Bank". Confirm with NSE which payload each one uses.

**Sample Request Json**

```json
{
  "nft_change of bank_account_details ": [
    {
      "AMC_CODE": "",
      "FOLIO_NO": "",
      "FH_NAME ": "",
      "TAX_NUMBER": "",
      "DOC_TYPE": "",
      "TWOFA_AUTH": "",
      "IMG_REF_NO": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "AB1_ACT_NO": "",
      "AB1_HLD_NA": "",
      "AB1_IFS_CD": "",
      "AB1_ACT_TY": "",
      "AB1_NAME": "",
      "AB1_BR_NAM": "",
      "AB2_ACT_NO": "",
      "AB2_HLD_NA": "",
      "AB2_IFS_CD": "",
      "AB2_ACT_TY": "",
      "AB2_NAME": "",
      "AB2_BR_NAM": "",
      "AB3_ACT_NO": "",
      "AB3_HLD_NA": "",
      "AB3_IFS_CD": "",
      "AB3_ACT_TY": "",
      "AB3_NAME": "",
      "AB3_BR_NAM": "",
      "AB4_ACT_NO": "",
      "AB4_HLD_NA": "",
      "AB4_IFS_CD": "",
      "AB4_ACT_TY": "",
      "AB4_NAME": "",
      "AB4_BR_NAM": "",
      "AB5_ACT_NO": "",
      "AB5_HLD_NA": "",
      "AB5_IFS_CD": "",
      "AB5_ACT_TY": "",
      "AB5_NAME": "",
      "AB5_BR_NAM": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "Message": "NFT - change of Bank account record added successfully.",
  "Status": "Success"
}
```

---

## 71. Change of Dividend

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/COD`  

PDF page: 211

**Sample Request Json**

```json
{
  "nft_change of dividend_details ": [
    {
      "AMC_CODE": "",
      "FOLIO_NO": "",
      "FH_NAME": "",
      "TAX_NUMBER": "",
      "DOC_TYPE": "",
      "TWOFA_AUTH": "",
      "IMG_REF_NO": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "SCH_CODE": "",
      "REINV_TAG": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "Message": "NFT - Change of Dividend record Added successfully.",
  "Status": "Success"
}
```

---

## 72. Change of Broker

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/COB`  

PDF page: 214

> Note: The request key is printed as `nft_ change of broker_details` (with spaces) in the doc. Confirm the exact key with NSE.

**Sample Request Json**

```json
{
  "nft_ change of broker_details": [
    {
      "AMC_CODE": "",
      "FOLIO_NO": "",
      "FH_NAME": "",
      "TAX_NUMBER": "",
      "DOC_TYPE": "",
      "TWOFA_AUTH": "",
      "IMG_REF_NO": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "BROKE_CD": "",
      "SBBR_CODE": "",
      "EUIN": "",
      "RIA_CODE": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": ""
    }
  ]
}
```

**SUCCESS**

```json
{
  "Message": "NFT - Change of broker record Added successfully.",
  "Status": "Success"
}
```

**FAILED**

```json
{
  "Message": "ERROR MESSAGE"
}
```

---

## 73. Change of Contact

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/COC`  

PDF page: 218

**Sample Request Json**

```json
{
  "nft_change_of contact_details": [
    {
      "AMC_CODE": "",
      "FOLIO_NO": "",
      "FH_NAME": "",
      "TAX_NUMBER": "",
      "DOC_TYPE": "",
      "TWOFA_AUTH": "",
      "IMG_REF_NO": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "J1_EMAIL": "",
      "J1_MOBILE": "",
      "J2_EMAIL": "",
      "J2_MOBILE": "",
      "PH_EMA_DEC": "",
      "PH_MOB_DEC": "",
      "J1_EMA_DEC": "",
      "J1_MOB_DEC": "",
      "J2_EMA_DEC": "",
      "J2_MOB_DEC": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "Message": "NFT - Change of Contact Record Added successfully.",
  "Status": "Success"
}
```

---

## 74. Consolidation of Folio

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/COF`  

PDF page: 222

**Sample Request Json**

```json
{
  "nft_consolidation of folio_details": [
    {
      "AMC_CODE": "",
      "FOLIO_NO": "",
      "FH_NAME": "",
      "TAX_NUMBER": "",
      "DOC_TYPE": "",
      "TWOFA_AUTH": "",
      "IMG_REF_NO": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "SRC_FOLIO": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "Message": "NFT - Consolidation of Folio Record Added successfully.",
  "Status": "Success"
}
```

---

## 75. Change of Bank

**POST** `https://{{API_URL}}/nsemfdesk/api/v1/NFT/COA`  

PDF page: 225

> Note: Same endpoint as section 70 in the doc (`/api/v1/NFT/COA`). Confirm with NSE.

**Sample Request Json**

```json
{
  "nft_change of bank_account_details ": [
    {
      "AMC_CODE": "",
      "FOLIO_NO": "",
      "FH_NAME": "",
      "TAX_NUMBER": "",
      "DOC_TYPE": "",
      "TWOFA_AUTH": "",
      "IMG_REF_NO": "",
      "EMAIL": "",
      "MOBILE_NO": "",
      "PB_ACT_NO": "",
      "PB_HLD_NAM": "",
      "PB_IFSC_CD": "",
      "PB_ACT_TY": "",
      "PB_NAM": "",
      "PB_BR_NAM": "",
      "Filler_1": "",
      "Filler_2": "",
      "Filler_3": "",
      "Filler_4": "",
      "Filler_5": "",
      "Filler_6": "",
      "Filler_7": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "Message": "NFT - change of Bank account record added successfully.",
  "Status": "Success"
}
```

---

## 76. NFT Image Upload API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/fileupload/NFTIMAGE`  

PDF page: 229

**Sample Request Json**

```json
{
  "img_name": "22202_KUDPC3565H_NOM_24072025_000024.tiff",
  "img_data": "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyA+PgplbmRvYmoKdHJhaWxlcgo8PD4+CiUlRU9G"
}
```

**Sample Response Json**

```json
{
  "img_name": "22202_KUDPC3565H_NOM_24072025_000024.tiff",
  "message": "Uploaded successfully",
  "status": "SUCCESS"
}
```

---

## 77. SIP Modification

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/modification/product/SIP_MOD`  

PDF page: 230

**Sample Request Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202603131000005",
      "primary_holder_email": "parixit@myCompany.in",
      "primary_holder_mobile": "",
      "sub_broker_code": "",
      "sub_broker_arn": "",
      "euin_number": "",
      "folio_no": "",
      "trans_mode": "",
      "amount": "10000",
      "units": "",
      "remarks": "",
      "send_2fa": "Y",
      "send_comm": "Y",
      "filler_1": "",
      "filler_2": "",
      "member_unique_id": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202603131000005",
      "primary_holder_email": "PARIXIT@myCompany.IN",
      "primary_holder_mobile": " ",
      "sub_broker_code": " ",
      "sub_broker_arn": " ",
      "euin_number": " ",
      "folio_no": " ",
      "trans_mode": " ",
      "amount": "10000",
      "remarks": " ",
      "send_2fa": "Y",
      "send_comm": "Y",
      "filler_1": " ",
      "filler_2": " ",
      "member_unique_id": " ",
      "status": "MODIFICATION_SUCCESS",
      "status_remarks": " "
    }
  ]
}
```

---

## 78. XSIP Modification

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/modification/product/XSIP_MOD`  

PDF page: 232

**Sample Request Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202604061000006",
      "primary_holder_email": "parixit@myCompany.in",
      "primary_holder_mobile": "9898571234",
      "sub_broker_code": "",
      "sub_broker_arn": "",
      "euin_number": "",
      "folio_no": "",
      "trans_mode": "",
      "amount": "3000",
      "units": "",
      "remarks": "",
      "send_2fa": "Y",
      "send_comm": "Y",
      "filler_1": "",
      "filler_2": "",
      "member_unique_id": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202604061000006",
      "primary_holder_email": "PARIXIT@myCompany.IN",
      "primary_holder_mobile": "9898571234",
      "sub_broker_code": " ",
      "sub_broker_arn": " ",
      "euin_number": " ",
      "folio_no": " ",
      "trans_mode": " ",
      "amount": "3000",
      "remarks": " ",
      "send_2fa": "Y",
      "send_comm": "Y",
      "filler_1": " ",
      "filler_2": " ",
      "member_unique_id": " ",
      "status": "MODIFICATION_SUCCESS",
      "status_remarks": " "
    }
  ]
}
```

---

## 79. STP Modification

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/modification/product/STP_MOD`  

PDF page: 235

**Sample Request Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202405291000021",
      "primary_holder_email": "",
      "primary_holder_mobile": "",
      "sub_broker_code": "",
      "sub_broker_arn": "",
      "euin_number": "",
      "folio_no": "",
      "trans_mode": "",
      "amount": "2000",
      "units": "",
      "remarks": "",
      "send_2fa": "",
      "send_comm": "",
      "filler_1": "",
      "filler_2": "",
      "member_unique_id": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202405291000021",
      "primary_holder_email": " ",
      "primary_holder_mobile": " ",
      "sub_broker_code": " ",
      "sub_broker_arn": " ",
      "euin_number": " ",
      "folio_no": " ",
      "trans_mode": " ",
      "amount": "2000",
      "units": " ",
      "remarks": " ",
      "send_2fa": " ",
      "send_comm": " ",
      "filler_1": " ",
      "filler_2": " ",
      "member_unique_id": " ",
      "status": "MODIFICATION_SUCCESS",
      "status_remarks": " "
    }
  ]
}
```

---

## 80. SWP Modification

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/modification/product/SWP_MOD`  

PDF page: 237

**Sample Request Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202406041000002",
      "primary_holder_email": "user@gmail.com",
      "primary_holder_mobile": "9574898779",
      "sub_broker_code": "",
      "sub_broker_arn": "",
      "euin_number": "E399871",
      "folio_no": "",
      "trans_mode": "",
      "amount": "3000",
      "units": "",
      "remarks": "",
      "send_2fa": "Y",
      "send_comm": "Y",
      "filler_1": "",
      "filler_2": "",
      "member_unique_id": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "mod_data": [
    {
      "sys_reg_no": "202406041000002",
      "primary_holder_email": "USER@GMAIL.COM",
      "primary_holder_mobile": "9574898779",
      "sub_broker_code": " ",
      "sub_broker_arn": " ",
      "euin_number": "E399871",
      "folio_no": " ",
      "trans_mode": " ",
      "amount": "3000",
      "units": " ",
      "remarks": " ",
      "send_2fa": "Y",
      "send_comm": "Y",
      "filler_1": " ",
      "filler_2": " ",
      "member_unique_id": " ",
      "status": "MODIFICATION_SUCCESS",
      "status_remarks": " "
    }
  ]
}
```

---

## 81. SIP AMC PAUSE SERVICE API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/registration/SIP_AMC_PAUSE`  

PDF page: 240

**Sample Request Json**

```json
{
  "pause_data": [
    {
      "client_code": "NDNTUCC76",
      "reg_type": "SIP",
      "sip_reg_no": "202508141000010",
      "modification_type": "PAUSE",
      "no_of_installments": "10",
      "pause_from": "16/01/2026",
      "filler_1": "",
      "filler_2": "",
      "filler_3": "",
      "filler_4": ""
    }
  ]
}
```

**Sample Response Json**

```json
{
  "pause_data": [
    {
      "registration_no": "202508141000010",
      "nse_remarks": "Pause Request posted successfully.",
      "status_flag": "0",
      "filler": " ",
      "request_id": "567"
    }
  ]
}
```

---

## 82. SIP AMC PAUSE REPORT API

**POST** `https://{{API_URL}}/nsemfdesk/api/v2/reports/SIP_AMC_PAUSE`  

PDF page: 241

**Sample Request Json**

```json
{
  "from_date": "",
  "to_date": "",
  "client_code": "NDNTUCC76",
  "registration_no": "202508201001017",
  "modification_type": "",
  "request_id": ""
}
```

Doc comments: PAUSE, UNPAUSE

**Sample Response Json**

```json
{
  "response_status": "S",
  "response_data_total": "2",
  "report_data": [
    {
      "client_code": "NDNTUCC76",
      "sip_registration_no": "202508201001017",
      "scheme_code": "IOGP",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "amount": "2000",
      "sip_start_date": "25/09/2025",
      "sip_end_date": "24/08/2035",
      "no_of_instalments_paused": "10",
      "date_of_activation": "15/01/2026",
      "pause_from_date": "15/01/2026",
      "pause_to_date": "15/11/2026",
      "request_id": "552",
      "entry_by": "ADMIN",
      "modified_date": "09/01/2026",
      "modified_instalments": "9"
    },
    {
      "client_code": "NDNTUCC76",
      "sip_registration_no": "202508201001017",
      "scheme_code": "IOGP",
      "scheme_name": "AXIS CREDIT RISK FUND GROWTH",
      "amount": "2000",
      "sip_start_date": "25/09/2025",
      "sip_end_date": "24/08/2035",
      "no_of_instalments_paused": "10",
      "date_of_activation": "16/01/2026",
      "pause_from_date": "16/01/2026",
      "pause_to_date": "16/11/2026",
      "request_id": "557",
      "entry_by": "ADMIN",
      "modified_date": "09/01/2026",
      "modified_instalments": "8"
    }
  ],
  "error_remark": ""
}
```
