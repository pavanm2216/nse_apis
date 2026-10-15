"""
NSE Mutual Fund API - Full Flow Tests
Runs against UAT: https://nseinvestuat.nseindia.com
Usage: pytest test_api.py -v
"""
import pytest
import httpx
import asyncio
from auth.nse_auth import get_auth_headers
from config import settings

BASE = "http://165.22.218.229:8000/api/v1"
TIMEOUT = 30

# ---------------------------------------------------------------------------
# Shared test data — adjust client_code to a valid UAT UCC
# ---------------------------------------------------------------------------
CLIENT_CODE = "NDNTUCC76"
TEST_PAN = "ABCDE1234F"
TEST_SCHEME_CODE = "IOGP"   # Axis Credit Risk Fund Growth (seen in pause report sample)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def post(url: str, payload: dict) -> httpx.Response:
    return httpx.post(f"{BASE}{url}", json=payload, timeout=TIMEOUT)


def get(url: str) -> httpx.Response:
    return httpx.get(f"{BASE}{url}", timeout=TIMEOUT)


# ===========================================================================
# PHASE 0 — Infrastructure
# ===========================================================================
class TestInfrastructure:

    def test_health_check(self):
        r = httpx.get("http://127.0.0.1:8000/health", timeout=10)
        assert r.status_code == 200
        assert r.json()["status"] == "ok"

    def test_auth_headers_generated(self):
        headers = get_auth_headers()
        assert "Authorization" in headers
        assert headers["Authorization"].startswith("BASIC ")
        assert "memberId" in headers
        assert headers["Content-Type"] == "application/json"

    def test_auth_headers_unique_each_call(self):
        """Each call must produce a different encrypted password (random nonce)."""
        h1 = get_auth_headers()["Authorization"]
        h2 = get_auth_headers()["Authorization"]
        assert h1 != h2


# ===========================================================================
# PHASE 1 — Client Onboarding
# ===========================================================================
class TestClientOnboarding:

    def test_ucc_register(self):
        payload = {
            "reg_details": [{
                "client_code": CLIENT_CODE,
                "primary_holder_first_name": "TEST",
                "primary_holder_last_name": "USER",
                "primary_holder_pan": TEST_PAN,
                "tax_status": "01",
                "holding_nature": "SI",
                "primary_holder_dob_incorporation": "01/01/1990",
                "occupation_code": "01",
                "account_type_1": "SB",
                "account_no_1": "123456789012",
                "ifsc_code_1": "HDFC0001234",
                "default_bank_flag_1": "Y",
                "address_1": "Test Address Line 1",
                "city": "Mumbai",
                "state": "MH",
                "pincode": "400001",
                "country": "IN",
                "indian_mobile_no": "9999999999",
                "email": "test@example.com",
                "primary_holder_kyc_type": "K",
                "nomination_opt": "N",
            }]
        }
        r = post("/ucc/register", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"
        if r.status_code == 200:
            data = r.json()
            assert "reg_details" in data

    def test_kyc_fresh_register(self):
        payload = {
            "pan_no": TEST_PAN,
            "client_code": CLIENT_CODE,
            "mobile_no": "9999999999",
            "email": "test@example.com"
        }
        r = post("/registration/kyc-fresh-register", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_client_kyc_report(self):
        payload = {
            "client_code": CLIENT_CODE,
            "pan_no": TEST_PAN
        }
        r = post("/reports/client-kyc", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_client_master_report(self):
        payload = {"client_code": CLIENT_CODE}
        r = post("/reports/client-master", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 2 — Scheme Discovery
# ===========================================================================
class TestSchemeDiscovery:

    def test_scheme_master_download(self):
        payload = {"file_type": "SCHEME_MASTER"}
        r = post("/reports/master-download", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_nav_download(self):
        payload = {"file_type": "NAV"}
        r = post("/reports/master-download", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 3 — Lumpsum Purchase Flow
# ===========================================================================
class TestLumpsumPurchase:

    def test_place_purchase_order(self):
        payload = {
            "transaction_details": [{
                "client_code": CLIENT_CODE,
                "scheme_code": TEST_SCHEME_CODE,
                "trxn_type": "P",
                "buy_sell_type": "FRESH",
                "order_amount": "5000",
                "demat_physical": "P",
                "kyc_flag": "Y",
                "euin_declaration": "N",
                "mobile_no": "9999999999",
                "email": "test@example.com",
            }]
        }
        r = post("/order/entry", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"
        if r.status_code == 200:
            data = r.json()
            assert "transaction_details" in data
            # store order id for payment test
            orders = data["transaction_details"]
            if orders and orders[0].get("trxn_order_id"):
                TestLumpsumPurchase.order_id = orders[0]["trxn_order_id"]

    def test_purchase_order_max_50_validation(self):
        payload = {
            "transaction_details": [
                {"client_code": CLIENT_CODE, "scheme_code": TEST_SCHEME_CODE,
                 "trxn_type": "P", "order_amount": "1000"}
                for _ in range(51)
            ]
        }
        r = post("/order/entry", payload)
        assert r.status_code == 400
        assert "50" in r.text

    def test_order_status_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        week_ago = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y")
        payload = {
            "from_date": week_ago,
            "to_date": today,
            "trans_type": "P",
            "order_type": "FRESH",
            "sub_order_type": "NORMAL",
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/order-status", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_provisional_orders_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        week_ago = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y")
        payload = {
            "from_date": week_ago,
            "to_date": today,
            "trans_type": "P",
            "order_type": "FRESH",
            "sub_order_type": "NORMAL",
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/provisional-orders", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_allotment_statement(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        month_ago = (date.today() - timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "from_date": month_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/allotment-statement", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 4 — Payment
# ===========================================================================
class TestPayment:

    def test_purchase_payment_upi(self):
        payload = {
            "payment_mode": "UPI",
            "client_code": CLIENT_CODE,
            "order_ids": "TEST_ORDER_001",
            "vpa": "test@upi",
            "callback_url": "https://example.com/callback"
        }
        r = post("/payments/purchase", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_upi_status_check(self):
        payload = {
            "nse_upi_ref_no": "NSE123456",
            "client_code": CLIENT_CODE
        }
        r = post("/payments/upi-status", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_get_short_url_link(self):
        payload = {
            "client_code": CLIENT_CODE,
            "order_id": "TEST_ORDER_001"
        }
        r = post("/communication/get-link", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 5 — Mandate
# ===========================================================================
class TestMandate:

    def test_mandate_registration(self):
        payload = {
            "reg_data": [{
                "client_code": CLIENT_CODE,
                "account_no": "123456789012",
                "ifsc_code": "HDFC0001234",
                "account_type": "SB",
                "amount": "50000",
                "mandate_type": "NACH",
                "start_date": "01/01/2025",
                "end_date": "31/12/2035",
            }]
        }
        r = post("/mandate/register", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_mandate_status_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        month_ago = (date.today() - timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "from_date": month_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/mandate-status", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 6 — SIP Flow
# ===========================================================================
class TestSIPFlow:

    def test_sip_register(self):
        from datetime import date, timedelta
        start = (date.today() + timedelta(days=10)).strftime("%d/%m/%Y")
        payload = {
            "reg_data": [{
                "client_code": CLIENT_CODE,
                "scheme_code": TEST_SCHEME_CODE,
                "transaction_mode": "P",
                "start_date": start,
                "frequency_type": "MONTHLY",
                "no_of_installments": "12",
                "installment_amount": "1000",
                "first_order_today": "N",
                "euin_declaration": "N",
                "mobile": "9999999999",
                "email": "test@example.com",
            }]
        }
        r = post("/sip/register", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"
        if r.status_code == 200:
            data = r.json()
            assert "reg_data" in data

    def test_sip_registration_report(self):
        payload = {"client_code": CLIENT_CODE}
        r = post("/reports/sip-registration", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_installment_due_report(self):
        payload = {"client_code": CLIENT_CODE}
        r = post("/reports/sip-installment-due", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_modification(self):
        payload = {
            "mod_data": [{
                "sys_reg_no": "202405291000021",
                "amount": "2000",
            }]
        }
        r = post("/modification/sip", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_pause(self):
        from datetime import date, timedelta
        future = (date.today() + timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "pause_data": [{
                "sip_reg_no": "202405291000021",
                "effective_date": future,
                "pause_flag": "Y",
            }]
        }
        r = post("/registration/sip-xsip-pause", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_amc_pause(self):
        from datetime import date, timedelta
        future = (date.today() + timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "pause_data": [{
                "client_code": CLIENT_CODE,
                "reg_type": "SIP",
                "sip_reg_no": "202405291000021",
                "modification_type": "PAUSE",
                "no_of_installments": "3",
                "pause_from": future,
            }]
        }
        r = post("/sip-amc-pause/pause", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_amc_pause_report(self):
        payload = {
            "client_code": CLIENT_CODE,
            "registration_no": "202405291000021",
        }
        r = post("/sip-amc-pause/report", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_cancellation(self):
        payload = {
            "can_data": [{
                "client_code": CLIENT_CODE,
                "sip_reg_no": "202405291000021",
                "remarks": "Test cancellation",
            }]
        }
        r = post("/sip-cancellation/cancel", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_sip_cancellation_report(self):
        payload = {"client_code": CLIENT_CODE}
        r = post("/reports/sip-cancellation", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 7 — STP / SWP Flow
# ===========================================================================
class TestSTPSWPFlow:

    def test_stp_register(self):
        from datetime import date, timedelta
        start = (date.today() + timedelta(days=10)).strftime("%d/%m/%Y")
        payload = {
            "reg_data": [{
                "client_code": CLIENT_CODE,
                "from_scheme_code": TEST_SCHEME_CODE,
                "to_scheme_code": "IOGPD",
                "buy_sell_type": "FRESH",
                "transaction_mode": "P",
                "start_date": start,
                "frequency_type": "MONTHLY",
                "no_of_transfers": "6",
                "installment_amount": "1000",
                "euin_declaration": "N",
            }]
        }
        r = post("/stp/register", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_stp_modification(self):
        payload = {
            "mod_data": [{
                "sys_reg_no": "202405291000021",
                "amount": "2000",
            }]
        }
        r = post("/stp-modification/modify", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_stp_cancellation(self):
        payload = {
            "can_data": [{
                "client_code": CLIENT_CODE,
                "stp_reg_no": "202405291000021",
                "remarks": "Test cancellation",
            }]
        }
        r = post("/stp-cancellation/cancel", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_stp_registration_report(self):
        payload = {"client_code": CLIENT_CODE}
        r = post("/reports/stp-registration", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_swp_register(self):
        from datetime import date, timedelta
        start = (date.today() + timedelta(days=10)).strftime("%d/%m/%Y")
        payload = {
            "reg_data": [{
                "client_code": CLIENT_CODE,
                "scheme_code": TEST_SCHEME_CODE,
                "trans_mode": "P",
                "start_date": start,
                "frequency_type": "MONTHLY",
                "no_of_withdrawals": "6",
                "installment_amount": "1000",
                "euin_declaration": "N",
            }]
        }
        r = post("/swp/register", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_swp_modification(self):
        payload = {
            "mod_data": [{
                "sys_reg_no": "202406041000002",
                "amount": "3000",
            }]
        }
        r = post("/swp-modification/modify", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_swp_cancellation(self):
        payload = {
            "can_data": [{
                "client_code": CLIENT_CODE,
                "swp_reg_no": "202406041000002",
                "remarks": "Test cancellation",
            }]
        }
        r = post("/cancellation/swp", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_swp_registration_report(self):
        payload = {"client_code": CLIENT_CODE}
        r = post("/reports/swp-registration", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 8 — Redemption
# ===========================================================================
class TestRedemption:

    def test_place_redemption_order(self):
        payload = {
            "transaction_details": [{
                "client_code": CLIENT_CODE,
                "scheme_code": TEST_SCHEME_CODE,
                "trxn_type": "R",
                "buy_sell_type": "FRESH",
                "all_units": "Y",
                "demat_physical": "P",
                "kyc_flag": "Y",
                "euin_declaration": "N",
                "mobile_no": "9999999999",
                "email": "test@example.com",
            }]
        }
        r = post("/order/entry", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_redemption_statement(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        month_ago = (date.today() - timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "from_date": month_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/redemption-statement", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_redemption_payout_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        month_ago = (date.today() - timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "report_type": "D",
            "from_date": month_ago,
            "to_date": today,
        }
        r = post("/reports/redemption-payout", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_order_cancellation(self):
        payload = {
            "can_data": [{
                "client_code": CLIENT_CODE,
                "order_id": "TEST_ORDER_001",
                "remarks": "Test cancel",
            }]
        }
        r = post("/order-cancellation/cancel", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 9 — Switch
# ===========================================================================
class TestSwitch:

    def test_switch_order(self):
        payload = {
            "transaction_details": [{
                "client_code": CLIENT_CODE,
                "scheme_code": TEST_SCHEME_CODE,
                "to_scheme": "IOGPD",
                "trxn_type": "S",
                "buy_sell_type": "FRESH",
                "all_units": "Y",
                "demat_physical": "P",
                "kyc_flag": "Y",
                "euin_declaration": "N",
            }]
        }
        r = post("/switch/entry", payload)
        assert r.status_code in (200, 400, 422), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 10 — Transaction History Reports
# ===========================================================================
class TestTransactionReports:

    def test_transaction_detail_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        month_ago = (date.today() - timedelta(days=30)).strftime("%d/%m/%Y")
        payload = {
            "from_date": month_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/transaction-detail", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_order_lifecycle_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        week_ago = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y")
        payload = {
            "from_date": week_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/order-lifecycle", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_2fa_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        week_ago = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y")
        payload = {
            "from_date": week_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/2fa", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"

    def test_client_authorization_report(self):
        from datetime import date, timedelta
        today = date.today().strftime("%d/%m/%Y")
        week_ago = (date.today() - timedelta(days=7)).strftime("%d/%m/%Y")
        payload = {
            "from_date": week_ago,
            "to_date": today,
            "client_code": CLIENT_CODE,
        }
        r = post("/reports/client-authorization", payload)
        assert r.status_code in (200, 400), f"Unexpected: {r.status_code} {r.text[:300]}"


# ===========================================================================
# PHASE 11 — Input Validation (no NSE call needed)
# ===========================================================================
class TestValidation:

    def test_sip_max_50_validation(self):
        payload = {
            "reg_data": [
                {"client_code": CLIENT_CODE, "scheme_code": TEST_SCHEME_CODE}
                for _ in range(51)
            ]
        }
        r = post("/sip/register", payload)
        assert r.status_code == 400
        assert "50" in r.text

    def test_stp_max_50_validation(self):
        payload = {
            "reg_data": [
                {"client_code": CLIENT_CODE}
                for _ in range(51)
            ]
        }
        r = post("/stp/register", payload)
        assert r.status_code == 400

    def test_swp_max_50_validation(self):
        payload = {
            "reg_data": [
                {"client_code": CLIENT_CODE}
                for _ in range(51)
            ]
        }
        r = post("/swp/register", payload)
        assert r.status_code == 400

    def test_sip_cancellation_max_50_validation(self):
        payload = {
            "can_data": [
                {"client_code": CLIENT_CODE, "sip_reg_no": "123"}
                for _ in range(51)
            ]
        }
        r = post("/sip-cancellation/cancel", payload)
        assert r.status_code == 400

    def test_sip_amc_pause_max_50_validation(self):
        payload = {
            "pause_data": [
                {"client_code": CLIENT_CODE, "sip_reg_no": "123",
                 "modification_type": "PAUSE", "no_of_installments": "1"}
                for _ in range(51)
            ]
        }
        r = post("/sip-amc-pause/pause", payload)
        assert r.status_code == 400

    def test_invalid_json_body(self):
        r = httpx.post(
            f"{BASE}/order/entry",
            content="not json",
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert r.status_code == 422

    def test_missing_required_fields_payment(self):
        """payment_mode, client_code, order_ids are required."""
        r = post("/payments/purchase", {"payment_mode": "UPI"})
        assert r.status_code == 422
