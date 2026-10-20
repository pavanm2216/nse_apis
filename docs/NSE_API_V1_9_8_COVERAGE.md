# NSE API v1.9.8 coverage map

Audit date: 19 October 2026. Source: `NSEMF_API_Details_V1.9.8.pdf` (August 2026, 238 pages).

This is a static route-to-specification comparison. "Path matches" means the upstream URL matches the PDF; it does **not** certify request validation, response handling, persistence, authentication interoperability, or UAT success. PDF page numbers are one-based. Public paths include the `/api/v1` mount in `main.py`.

Mapped 84 public route/upstream pairs to 83 distinct upstream URLs. Found 82 distinct documented API URLs; 3 route/upstream pairs differ by case. Two local KYC aliases share one upstream operation. The PDF lists COA twice for different bank operations; COM is present in its NFT master but absent from its URL strings. Bank ELog upload is removed by the latest changelog. See [the audit](NSE_API_V1_9_8_AUDIT.md) for these exceptions.

## Administration

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/admin/change-api-secret` | `misc_services.py` | `v2/admin/CHANGE_API_SECRET` | 178 | Path matches |

## Clients

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/aof/image-upload` | `aof_image_upload.py` | `v2/fileupload/AOFIMG` | 94 | Path matches |
| `/api/v1/cancel-cheque/upload` | `cancel_cheque_upload.py` | `v2/fileupload/CANCELCHEQUE` | 98 | Path matches |
| `/api/v1/client-bank-detail/update` | `client_bank_detail.py` | `v2/registration/CLIENTBANKDTL` | 59 | Path matches |
| `/api/v1/communication/resend` | `communication.py` | `v2/registration/RESEND_COMM` | 73 | Path matches |
| `/api/v1/elog/upload` | `elog_upload.py` | `v2/registration/eLOG` | 96, 238 | Removed in v1.9.8 |
| `/api/v1/fatca/common-upload` | `fatca_common.py` | `v2/registration/FATCA_COMMON` | 83 | Path matches |
| `/api/v1/fatca/image-upload` | `fatca_image_upload.py` | `v2/fileupload/FATCAIMG` | 95 | Path matches |
| `/api/v1/fatca/upload` | `fatca_registration.py` | `v2/registration/FATCA` | 75 | Path matches |
| `/api/v1/ekyc/register` | `misc_services.py` | `v1/EKYC/EKYCREG` | 165 | Path matches |
| `/api/v1/nft/nominee` | `misc_services.py` | `v1/NFT/NOM` | 179 | Path matches |
| `/api/v1/nft/change-of-bank` | `misc_services.py` | `v1/NFT/COA` | 198 | Path matches |
| `/api/v1/nft/change-of-dividend` | `misc_services.py` | `v1/NFT/COD` | 204 | Path matches |
| `/api/v1/nft/change-of-broker` | `misc_services.py` | `v1/NFT/COB` | 207 | Path matches |
| `/api/v1/nft/change-of-contact` | `misc_services.py` | `v1/NFT/COC` | 210 | Path matches |
| `/api/v1/nft/consolidation-of-folio` | `misc_services.py` | `v1/NFT/COF` | 214 | Path matches |
| `/api/v1/nft/change-of-bank-single` | `misc_services.py` | `v1/NFT/COM` | 179, 217 | Spec conflict: COM / COA |
| `/api/v1/nft/image-upload` | `misc_services.py` | `v2/fileupload/NFTIMAGE` | 220 | Path matches |
| `/api/v1/registration/kyc-fresh-register` | `misc_services.py` | `v1/EKYC/EKYCREG` | 165 | Path matches |
| `/api/v1/poa/upload` | `poa_upload.py` | `v2/fileupload/POA_UPLOAD` | 97 | Path matches |
| `/api/v1/ucc/register` | `ucc.py` | `v2/registration/CLIENTCOMMON183` | 34 | Path matches |

## Orders

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/order/entry` | `order.py` | `v2/transaction/NORMAL` | 7 | Path matches |
| `/api/v1/order-cancellation/cancel` | `order_cancellation.py` | `v2/cancellation/ORDER_CAN` | 33 | Path matches |
| `/api/v1/switch/entry` | `switch.py` | `v2/transaction/SWITCH` | 11 | Path matches |

## Systematic investments

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/daily-xsip-cancellation/cancel` | `daily_xsip_cancellation.py` | `v2/cancellation/DAILY_XSIP_CAN` | 55 | Path matches |
| `/api/v1/cancellation/swp` | `misc_services.py` | `v2/cancellation/SWP_CAN` | 170 | Path matches |
| `/api/v1/registration/sip-xsip-pause` | `misc_services.py` | `v2/registration/XSIP_PAUSE` | 172 | Path matches |
| `/api/v1/modification/sip` | `misc_services.py` | `v2/modification/product/SIP_MOD` | 221 | Path matches |
| `/api/v1/modification/xsip` | `misc_services.py` | `v2/modification/product/XSIP_MOD` | 224 | Path matches |
| `/api/v1/sip/register` | `sip.py` | `v2/registration/product/SIP` | 21 | Path matches |
| `/api/v1/sip-amc-pause/pause` | `sip_amc_pause.py` | `v2/registration/SIP_AMC_PAUSE` | 231 | Path matches |
| `/api/v1/sip-cancellation/cancel` | `sip_cancellation.py` | `v2/cancellation/SIP_CAN` | 51 | Path matches |
| `/api/v1/sip-topup/register` | `sip_topup.py` | `v2/registration/product/SIP_TOPUP` | 19 | Path matches |
| `/api/v1/sip/umrn-mapping` | `sip_umrn_mapping.py` | `v2/registration/SIPUMRN` | 65 | Path matches |
| `/api/v1/stp/register` | `stp.py` | `v2/registration/product/STP` | 26 | Path matches |
| `/api/v1/stp-cancellation/cancel` | `stp_cancellation.py` | `v2/cancellation/STP_CAN` | 57 | Path matches |
| `/api/v1/stp-modification/modify` | `stp_modification.py` | `v2/modification/product/STP_MOD` | 226 | Path matches |
| `/api/v1/swp/register` | `swp.py` | `v2/registration/product/SWP` | 29 | Path matches |
| `/api/v1/swp-modification/modify` | `swp_modification.py` | `v2/modification/product/SWP_MOD` | 228 | Path matches |
| `/api/v1/xsip/register` | `xsip.py` | `v2/registration/product/XSIP` | 14 | Path matches |
| `/api/v1/xsip-cancellation/cancel` | `xsip_cancellation.py` | `v2/cancellation/XSIP_CAN` | 53 | Path matches |

## Mandates

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/mandate/image-upload` | `mandate_image_upload.py` | `v2/fileupload/MANDATEIMG` | 63 | Path matches |
| `/api/v1/mandate/register` | `mandate_registration.py` | `v2/registration/product/MANDATE` | 61 | Path matches |

## Payments

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/payments/purchase` | `misc_services.py` | `v2/payments/purchase_payment` | 166 | Path matches |
| `/api/v1/payments/upi-status` | `misc_services.py` | `v2/payments/upi_status_check` | 169 | Path matches |
| `/api/v1/utr/update` | `utr_update.py` | `v2/transaction/UTRUPDATE` | 64 | Path matches |

## Reports

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/communication/get-link` | `communication.py` | `v2/reports/GET_LINK` | 71 | Path matches |
| `/api/v1/reports/mandate-status` | `mandate_status_report.py` | `v2/reports/MANDATE_STATUS` | 70 | Path matches |
| `/api/v1/reports/member-fund-allocation/order-wise` | `member_fund_allocation.py` | `v2/reports/MEMBER_FUND_ALLOCATION/ORDER_WISE` | 99 | Path matches |
| `/api/v1/reports/member-fund-allocation/age-wise` | `member_fund_allocation.py` | `v2/reports/MEMBER_FUND_ALLOCATION/AGE_WISE` | 101 | Path matches |
| `/api/v1/reports/securities-delivery-shortage` | `misc_reports.py` | `v2/reports/SECURITIES_DELIVERY_AND_SHORTAGE_REPORT` | 116 | Path matches |
| `/api/v1/reports/2fa` | `misc_reports.py` | `v2/reports/2fa` | 118 | Case differs |
| `/api/v1/reports/client-authorization` | `misc_reports.py` | `v2/reports/client_authorization` | 119 | Case differs |
| `/api/v1/reports/client-detail` | `misc_reports.py` | `v2/reports/CLIENT_DETAIL_REPORT` | 122 | Path matches |
| `/api/v1/reports/order-lifecycle` | `misc_reports.py` | `v2/reports/order_lifecycle` | 126 | Case differs |
| `/api/v1/reports/transaction-detail` | `misc_reports.py` | `v2/reports/TRANSACTION_DETAIL_REPORT` | 128 | Path matches |
| `/api/v1/reports/fatca` | `misc_reports.py` | `v2/reports/FATCA_REPORT` | 133 | Path matches |
| `/api/v1/reports/aof-image-upload` | `misc_reports.py` | `v2/reports/AOF_IMAGE_UPLOAD_REPORT` | 135 | Path matches |
| `/api/v1/reports/elog-upload` | `misc_reports.py` | `v2/reports/ELOG_UPLOAD_REPORT` | 137 | Path matches |
| `/api/v1/reports/sip-registration` | `misc_reports.py` | `v2/reports/SIP_REG_REPORT` | 139 | Path matches |
| `/api/v1/reports/sip-cancellation` | `misc_reports.py` | `v2/reports/SIP_CAN_REPORT` | 141 | Path matches |
| `/api/v1/reports/sip-installment-due` | `misc_reports.py` | `v2/reports/SIP_INST_DUE_REPORT` | 142 | Path matches |
| `/api/v1/reports/sip-topup` | `misc_reports.py` | `v2/reports/SIP_TOPUP_REPORT` | 144 | Path matches |
| `/api/v1/reports/stepup-registration` | `misc_reports.py` | `v2/reports/STEPUP_REG_REPORT` | 145 | Path matches |
| `/api/v1/reports/xsip-registration` | `misc_reports.py` | `v2/reports/XSIP_REG_REPORT` | 147 | Path matches |
| `/api/v1/reports/xsip-cancellation` | `misc_reports.py` | `v2/reports/XSIP_CAN_REPORT` | 149 | Path matches |
| `/api/v1/reports/xsip-installment-due` | `misc_reports.py` | `v2/reports/XSIP_INST_DUE_REPORT` | 150 | Path matches |
| `/api/v1/reports/xsip-topup` | `misc_reports.py` | `v2/reports/XSIP_TOPUP_REPORT` | 152 | Path matches |
| `/api/v1/reports/stp-registration` | `misc_reports.py` | `v2/reports/STP_REG_REPORT` | 153 | Path matches |
| `/api/v1/reports/stp-cancellation` | `misc_reports.py` | `v2/reports/STP_CAN_REPORT` | 155 | Path matches |
| `/api/v1/reports/stp-installment-due` | `misc_reports.py` | `v2/reports/STP_INST_DUE_REPORT` | 156 | Path matches |
| `/api/v1/reports/swp-registration` | `misc_reports.py` | `v2/reports/SWP_REG_REPORT` | 158 | Path matches |
| `/api/v1/reports/swp-cancellation` | `misc_reports.py` | `v2/reports/SWP_CAN_REPORT` | 160 | Path matches |
| `/api/v1/reports/swp-installment-due` | `misc_reports.py` | `v2/reports/SWP_INST_DUE_REPORT` | 161 | Path matches |
| `/api/v1/reports/client-kyc` | `misc_reports.py` | `v2/reports/CLIENT_KYC_REPORT` | 164 | Path matches |
| `/api/v1/reports/client-master` | `misc_services.py` | `v2/reports/client_master_report` | 173 | Path matches |
| `/api/v1/reports/provisional-orders` | `order_status_report.py` | `v2/reports/PROV_ORDERS` | 66 | Path matches |
| `/api/v1/reports/order-status` | `order_status_report.py` | `v2/reports/ORDER_STATUS` | 66 | Path matches |
| `/api/v1/reports/redemption-payout` | `redemption_payout.py` | `v2/reports/REDEMPTION_PAYOUT` | 104 | Path matches |
| `/api/v1/reports/redemption-payout-non-demat` | `redemption_payout.py` | `v2/reports/REDEMPTION_PAYOUT_NON_DEMAT` | 106 | Path matches |
| `/api/v1/sip-amc-pause/report` | `sip_amc_pause.py` | `v2/reports/SIP_AMC_PAUSE` | 232 | Path matches |
| `/api/v1/reports/redemption-statement` | `statement_reports.py` | `v2/reports/REDEMPTION_STATEMENT` | 108 | Path matches |
| `/api/v1/reports/allotment-statement` | `statement_reports.py` | `v2/reports/ALLOTMENT_STATEMENT` | 111 | Path matches |

## Masters

| Local POST path | Router | NSE path (after `/nsemfdesk/api/`) | PDF page | Static status |
|---|---|---|---|---|
| `/api/v1/reports/master-download` | `misc_reports.py` | `v2/reports/MASTER_DOWNLOAD` | 163 | Path matches |

## Documented paths with no case-insensitive route match

None found.

Authentication is separate: `/api/v1/auth/login` issues a local JWT; `auth/nse_auth.py` builds NSE Basic authorization for upstream calls. `/health` and the hidden outbound-IP diagnostic are application endpoints, not NSE operations.
