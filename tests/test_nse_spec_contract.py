"""v1.9.8 audit regressions. Run through scripts/run_offline_tests.py."""
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError
import pytest


def test_documented_order_success_is_persisted():
    """PDF pp. 9-10: TRXN SUCCESS is an accepted order-entry result."""
    from database import get_db
    from routers.order import router

    db = AsyncMock()
    db.add = MagicMock()
    query_result = MagicMock()
    query_result.scalar_one_or_none.return_value = None
    db.execute.return_value = query_result

    async def fake_db():
        yield db

    response = MagicMock(status_code=200)
    response.json.return_value = {"transaction_details": [{
        "trxn_order_id": "432160000001", "trxn_status": "TRXN SUCCESS",
        "scheme_code": "AXBDGP-GR", "client_code": "TEST001",
    }]}
    upstream = AsyncMock()
    upstream.__aenter__.return_value = upstream
    upstream.post.return_value = response
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = fake_db
    with patch("routers.order.get_nse_client", return_value=upstream), patch(
        "routers.order.get_auth_headers", return_value={}
    ), TestClient(app) as client:
        result = client.post("/order/entry", json={"transaction_details": [{
            "scheme_code": "AXBDGP-GR", "trxn_type": "P",
            "buy_sell_type": "FRESH", "client_code": "TEST001",
            "demat_physical": "C", "order_amount": "2000",
            "kyc_flag": "Y", "euin_declaration": "N",
        }]})
    assert result.status_code == 200
    assert db.add.call_count == 1, "Documented TRXN SUCCESS was not persisted"
    db.commit.assert_awaited_once()


@pytest.mark.parametrize("model_module,model_name", [
    ("schemas.sip", "SIPRegistrationRequest"),
    ("schemas.stp", "STPRegistrationRequest"),
])
def test_registration_rejects_missing_mandatory_fields(model_module, model_name):
    """PDF pp. 21-24 and 26-28 require client, schemes and dates."""
    import importlib

    model = getattr(importlib.import_module(model_module), model_name)
    with pytest.raises(ValidationError):
        model.model_validate({"reg_data": [{}]})


def test_kyc_alias_forwards_documented_keys_and_preserves_link():
    """PDF p. 165: both KYC entry points must speak the same wire contract."""
    from routers.misc_services import router

    app = FastAPI()
    app.include_router(router)
    payload = {
        "amcCode": "B", "panNo": "ABCDE1234F",
        "mobileNo": "9000000000", "invEmail": "offline@example.invalid",
    }
    post = AsyncMock(return_value={"link": "https://example.invalid/kyc", "message": "OK"})
    with patch("routers.misc_services._post", post), TestClient(app) as client:
        response = client.post("/registration/kyc-fresh-register", json=payload)
    assert response.status_code == 200
    assert post.call_args.args[1] == payload
    assert response.json()["link"] == "https://example.invalid/kyc"


@pytest.mark.parametrize("constant,suffix", [
    ("NSE_2FA_URL", "/reports/2FA"),
    ("NSE_CLIENT_AUTH_URL", "/reports/CLIENT_AUTHORIZATION"),
    ("NSE_ORDER_LIFECYCLE_URL", "/reports/ORDER_LIFECYCLE"),
])
def test_report_url_matches_documented_case(constant, suffix):
    """PDF pp. 118, 119, 126 specify exact upstream path capitalization."""
    from routers import misc_reports

    assert getattr(misc_reports, constant).endswith(suffix)
