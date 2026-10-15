"""
Tests for NSE authentication header construction and order entry flow.
All NSE responses are mocked. No real credentials are used or logged.
No real financial orders are placed.
"""
import base64
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, call
from fastapi.testclient import TestClient
from fastapi import FastAPI


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _decode_auth_header(header_value: str) -> tuple[str, str]:
    """
    Splits 'BASIC <b64>' and decodes the credential portion.
    Returns (scheme, decoded_credentials) without logging either.
    """
    parts = header_value.split(" ", 1)
    assert len(parts) == 2, f"Expected 'SCHEME value', got: {header_value!r}"
    scheme, b64 = parts
    decoded = base64.b64decode(b64).decode("utf-8")
    return scheme, decoded


def _make_order_app():
    from routers.order import router as order_router
    app = FastAPI()
    app.include_router(order_router, prefix="/api/v1")
    return app


def _make_ucc_app():
    from routers.ucc import router as ucc_router
    app = FastAPI()
    app.include_router(ucc_router, prefix="/api/v1")
    return app


def _valid_order_payload(**overrides):
    base = {
        "scheme_code": "AXBDGP-GR",
        "trxn_type": "P",
        "buy_sell_type": "FRESH",
        "client_code": "K0281",
        "demat_physical": "C",
        "order_amount": "2000",
        "kyc_flag": "Y",
        "euin_declaration": "Y",
    }
    base.update(overrides)
    return {"transaction_details": [base]}


_MOCK_HEADERS = {
    "Authorization": "BASIC mock",
    "memberId": "1003338",
    "Content-Type": "application/json",
}


def _make_mock_db(commit_error: Exception | None = None):
    """Returns (mock_db_session, added_records_list)."""
    added_records = []
    mock_db = AsyncMock()
    mock_db.add = MagicMock(side_effect=lambda r: added_records.append(r))
    mock_db.commit = AsyncMock(side_effect=commit_error) if commit_error else AsyncMock()
    mock_db.rollback = AsyncMock()
    return mock_db, added_records


def _override_db(app: FastAPI, mock_db):
    """Override the get_db FastAPI dependency with a mock session."""
    from database import get_db

    async def _mock_get_db():
        yield mock_db

    app.dependency_overrides[get_db] = _mock_get_db


def _mock_nse_client(status_code: int, body: str):
    mock_response = MagicMock()
    mock_response.status_code = status_code
    mock_response.text = body
    import json as _json
    mock_response.json = MagicMock(return_value=_json.loads(body) if status_code == 200 else None)

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post = AsyncMock(return_value=mock_response)
    return mock_client


# ---------------------------------------------------------------------------
# 1. Auth header construction
# ---------------------------------------------------------------------------

class TestAuthHeaderConstruction:

    def test_scheme_is_BASIC(self):
        from auth.nse_auth import get_auth_headers
        headers = get_auth_headers()
        assert headers["Authorization"].startswith("BASIC "), \
            "Authorization header must start with 'BASIC '"

    def test_no_bearer_prefix(self):
        from auth.nse_auth import get_auth_headers
        headers = get_auth_headers()
        assert not headers["Authorization"].startswith("Bearer"), \
            "Authorization must NOT start with 'Bearer'"

    def test_member_id_present(self):
        from auth.nse_auth import get_auth_headers
        headers = get_auth_headers()
        assert "memberId" in headers
        assert headers["memberId"] == "1003338"

    def test_content_type_json(self):
        from auth.nse_auth import get_auth_headers
        headers = get_auth_headers()
        assert headers["Content-Type"] == "application/json"

    def test_accept_not_empty(self):
        from auth.nse_auth import get_auth_headers
        headers = get_auth_headers()
        assert headers.get("Accept", "") != "", "Accept header must not be empty"

    def test_credential_format_user_colon_password(self):
        """Decoded credential must be user_id:encrypted_password."""
        from auth.nse_auth import get_auth_headers
        from config import settings
        headers = get_auth_headers()
        scheme, decoded = _decode_auth_header(headers["Authorization"])
        assert scheme == "BASIC"
        assert decoded.startswith(settings.NSE_LOGIN_USER_ID + ":")

    def test_encrypted_password_is_base64(self):
        """The password portion must itself be valid base64 with iv::salt::aes format."""
        from auth.nse_auth import get_auth_headers
        from config import settings
        headers = get_auth_headers()
        _, decoded = _decode_auth_header(headers["Authorization"])
        user_id, encrypted_password = decoded.split(":", 1)
        inner = base64.b64decode(encrypted_password).decode("utf-8")
        parts = inner.split("::")
        assert len(parts) == 3, f"Encrypted password inner format must be iv::salt::aes, got {len(parts)} parts"

    def test_each_call_produces_different_token(self):
        """Every call must produce a fresh encrypted password (random IV + random number)."""
        from auth.nse_auth import get_auth_headers
        h1 = get_auth_headers()
        h2 = get_auth_headers()
        assert h1["Authorization"] != h2["Authorization"], \
            "Each call must produce a unique Authorization value"

    def test_get_nse_token_scheme(self):
        from auth.nse_auth import get_nse_token
        token = get_nse_token()
        assert token.startswith("BASIC "), "get_nse_token must return 'BASIC <value>'"


# ---------------------------------------------------------------------------
# 2. Login response
# ---------------------------------------------------------------------------

class TestLoginResponse:

    def test_login_returns_basic_token_type(self):
        from auth.nse_auth import get_nse_token
        token = get_nse_token()
        assert "BASIC" in token

    def test_login_token_not_forwarded_to_nse(self):
        """
        get_auth_headers() always rebuilds from .env — never from the login token.
        Both are BASIC but with different random encrypted passwords.
        """
        from auth.nse_auth import get_nse_token, get_auth_headers
        login_token = get_nse_token()
        nse_header = get_auth_headers()["Authorization"]
        assert login_token != nse_header


# ---------------------------------------------------------------------------
# 3. Request validation — 422
# ---------------------------------------------------------------------------

class TestRequestValidation:

    def test_empty_transaction_details_returns_422(self):
        with patch("routers.order.get_nse_client"), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json={"transaction_details": []})
                assert resp.status_code == 422

    def test_missing_scheme_code_returns_422(self):
        payload = {
            "transaction_details": [{
                "trxn_type": "P",
                "buy_sell_type": "FRESH",
                "client_code": "K0281",
                "demat_physical": "C",
                "order_amount": "2000",
                "kyc_flag": "Y",
                "euin_declaration": "Y",
            }]
        }
        with patch("routers.order.get_nse_client"), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=payload)
                assert resp.status_code == 422

    def test_empty_scheme_code_returns_422(self):
        with patch("routers.order.get_nse_client"), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload(scheme_code=""))
                assert resp.status_code == 422

    def test_max_50_orders_returns_400(self):
        payload = {
            "transaction_details": [
                {
                    "scheme_code": "AXBDGP-GR", "trxn_type": "P", "buy_sell_type": "FRESH",
                    "client_code": "K0281", "demat_physical": "C", "order_amount": "1000",
                    "kyc_flag": "Y", "euin_declaration": "N",
                }
                for _ in range(51)
            ]
        }
        with patch("routers.order.get_nse_client"), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=payload)
                assert resp.status_code == 400
                assert "50" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 4. Order Entry — 403 handling
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestOrderEntry403:

    async def test_order_entry_raises_403_on_nse_403(self):
        mock_client = _mock_nse_client(
            403,
            '{"status":"403 FORBIDDEN","error_type":"unauthorized",'
            '"message":"Invalid authorization header or IP Address not mapped with user."}'
        )
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 403
                assert "NSE 403" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 5. UCC Registration — 403 handling
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestUCCRegistration403:

    async def test_ucc_register_raises_403_on_nse_403(self):
        mock_client = _mock_nse_client(
            403,
            '{"status":"403 FORBIDDEN","error_type":"unauthorized","message":"NSE authentication failed"}'
        )
        with patch("routers.ucc.get_nse_client", return_value=mock_client), \
             patch("routers.ucc.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_ucc_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/ucc/register", json={
                    "reg_details": [{"client_code": "K0281", "primary_holder_first_name": "Test"}]
                })
                assert resp.status_code == 403
                assert "NSE 403" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 6. HTTP timeout and connection error handling
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestHTTPErrors:

    async def test_order_entry_connect_error_returns_502(self):
        import httpx
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=httpx.ConnectError("Connection refused"))

        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 502
                assert "Cannot connect to NSE" in resp.json()["detail"]

    async def test_order_entry_timeout_returns_504(self):
        import httpx
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=False)
        mock_client.post = AsyncMock(side_effect=httpx.TimeoutException("Timeout"))

        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(_make_order_app(), raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 504
                assert "timed out" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 7. Successful transaction response
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestSuccessfulTransaction:

    async def test_successful_order_returns_200_with_trxn_order_id(self):
        nse_body = (
            '{"transaction_details": [{'
            '"scheme_code": "AXBDGP-GR", "trxn_type": "P", "client_code": "K0281",'
            '"trxn_order_id": "ORD20240601001", "trxn_status": "ACCEPTED",'
            '"trxn_remark": "Order placed successfully"'
            '}]}'
        )
        mock_client = _mock_nse_client(200, nse_body)
        mock_db, _ = _make_mock_db()

        app = _make_order_app()
        _override_db(app, mock_db)
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(app, raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 200
                data = resp.json()
                assert "transaction_details" in data
                txn = data["transaction_details"][0]
                assert txn["trxn_order_id"] == "ORD20240601001"
                assert txn["trxn_status"] == "ACCEPTED"

    async def test_http_200_with_trxn_failed_is_not_success(self):
        """HTTP 200 from NSE with TRXN FAILED status must be surfaced, not treated as success."""
        nse_body = (
            '{"transaction_details": [{'
            '"scheme_code": "AXBDGP-GR", "trxn_type": "P", "client_code": "K0281",'
            '"trxn_order_id": "", "trxn_status": "TRXN FAILED",'
            '"trxn_remark": "Scheme Code is required."'
            '}]}'
        )
        mock_client = _mock_nse_client(200, nse_body)
        mock_db, _ = _make_mock_db()

        app = _make_order_app()
        _override_db(app, mock_db)
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(app, raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                # Backend returns 200 — frontend must inspect trxn_status
                assert resp.status_code == 200
                data = resp.json()
                txn = data["transaction_details"][0]
                assert txn["trxn_status"] == "TRXN FAILED"
                assert "Scheme Code is required" in txn["trxn_remark"]


# ---------------------------------------------------------------------------
# 8. 502 — oversized NSE response values
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestOversizedResponse:

    async def test_oversized_varchar1_field_returns_502(self):
        """NSE returning 'STRING' for a VARCHAR(1) column must yield HTTP 502."""
        nse_body = (
            '{"transaction_details": [{'
            '"scheme_code": "AXBDGP-GR", "trxn_type": "STRING",'
            '"client_code": "K0281", "trxn_status": "TRXN FAILED",'
            '"trxn_remark": "error"'
            '}]}'
        )
        mock_client = _mock_nse_client(200, nse_body)
        mock_db, _ = _make_mock_db()

        app = _make_order_app()
        _override_db(app, mock_db)
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(app, raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 502
                assert "exceeds" in resp.json()["detail"]


# ---------------------------------------------------------------------------
# 9. PostgreSQL persistence
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
class TestDatabasePersistence:

    async def test_successful_order_is_persisted_to_db(self):
        nse_body = (
            '{"transaction_details": [{'
            '"scheme_code": "AXBDGP-GR", "trxn_type": "P", "client_code": "K0281",'
            '"trxn_order_id": "ORD20240601001", "trxn_status": "ACCEPTED",'
            '"trxn_remark": "Order placed successfully"'
            '}]}'
        )
        mock_client = _mock_nse_client(200, nse_body)
        mock_db, added_records = _make_mock_db()

        app = _make_order_app()
        _override_db(app, mock_db)
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(app, raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 200
                mock_db.commit.assert_awaited_once()
                assert len(added_records) == 1
                record = added_records[0]
                assert record.trxn_order_id == "ORD20240601001"
                assert record.trxn_status == "ACCEPTED"

    async def test_failed_transaction_is_still_persisted(self):
        """Even a TRXN FAILED response must be saved to DB for audit."""
        nse_body = (
            '{"transaction_details": [{'
            '"scheme_code": "AXBDGP-GR", "trxn_type": "P", "client_code": "K0281",'
            '"trxn_order_id": "", "trxn_status": "TRXN FAILED",'
            '"trxn_remark": "Scheme Code is required."'
            '}]}'
        )
        mock_client = _mock_nse_client(200, nse_body)
        mock_db, added_records = _make_mock_db()

        app = _make_order_app()
        _override_db(app, mock_db)
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(app, raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 200
                mock_db.commit.assert_awaited_once()
                assert len(added_records) == 1
                assert added_records[0].trxn_status == "TRXN FAILED"

    async def test_db_error_returns_500_and_rolls_back(self):
        nse_body = (
            '{"transaction_details": [{'
            '"scheme_code": "AXBDGP-GR", "trxn_type": "P", "client_code": "K0281",'
            '"trxn_order_id": "ORD001", "trxn_status": "ACCEPTED", "trxn_remark": ""'
            '}]}'
        )
        mock_client = _mock_nse_client(200, nse_body)
        mock_db, _ = _make_mock_db(commit_error=Exception("DB connection lost"))

        app = _make_order_app()
        _override_db(app, mock_db)
        with patch("routers.order.get_nse_client", return_value=mock_client), \
             patch("routers.order.get_auth_headers", return_value=_MOCK_HEADERS):
            with TestClient(app, raise_server_exceptions=False) as client:
                resp = client.post("/api/v1/order/entry", json=_valid_order_payload())
                assert resp.status_code == 500
                assert "DB save failed" in resp.json()["detail"]
                mock_db.rollback.assert_awaited_once()
