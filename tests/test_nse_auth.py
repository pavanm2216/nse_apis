"""
Offline unit tests for auth/nse_auth.py PBKDF2 implementation.
No real NSE credentials or network calls are used.
"""
import base64
import hashlib
import os
from unittest.mock import patch

import pytest


FAKE_USER_ID     = "TESTUSER"
FAKE_API_SECRET  = "FAKESECRET123"
FAKE_LICENSE_KEY = "abcdef1234567890abcdef1234567890"  # 32-char hex string
FAKE_MEMBER_ID   = "9999999"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_module():
    """Import nse_auth with settings patched so no real .env is required."""
    from unittest.mock import MagicMock
    fake_settings = MagicMock()
    fake_settings.NSE_LOGIN_USER_ID  = FAKE_USER_ID
    fake_settings.NSE_API_SECRET     = FAKE_API_SECRET
    fake_settings.NSE_API_LICENSE_KEY = FAKE_LICENSE_KEY
    fake_settings.NSE_MEMBER_ID      = FAKE_MEMBER_ID
    with patch("auth.nse_auth.settings", fake_settings):
        import importlib
        import auth.nse_auth as m
        importlib.reload(m)
        m.settings = fake_settings
        return m


# ---------------------------------------------------------------------------
# _build_encrypted_password
# ---------------------------------------------------------------------------

def test_encrypted_password_three_segments():
    """Decoded combined string must have exactly 3 '::'-separated segments."""
    m = _get_module()
    enc = m._build_encrypted_password(FAKE_API_SECRET, FAKE_LICENSE_KEY)
    decoded = base64.b64decode(enc).decode("utf-8")
    parts = decoded.split("::")
    assert len(parts) == 3, f"Expected 3 segments, got {len(parts)}: {decoded}"


def test_encrypted_password_iv_is_16_bytes():
    """First segment (IV hex) must decode to exactly 16 bytes."""
    m = _get_module()
    enc = m._build_encrypted_password(FAKE_API_SECRET, FAKE_LICENSE_KEY)
    decoded = base64.b64decode(enc).decode("utf-8")
    iv_hex = decoded.split("::")[0]
    assert len(bytes.fromhex(iv_hex)) == 16


def test_encrypted_password_salt_is_16_bytes():
    """Second segment (salt hex) must decode to exactly 16 bytes."""
    m = _get_module()
    enc = m._build_encrypted_password(FAKE_API_SECRET, FAKE_LICENSE_KEY)
    decoded = base64.b64decode(enc).decode("utf-8")
    salt_hex = decoded.split("::")[1]
    assert len(bytes.fromhex(salt_hex)) == 16


def test_encrypted_password_third_segment_is_valid_base64():
    """Third segment must be valid base64 (the AES ciphertext)."""
    m = _get_module()
    enc = m._build_encrypted_password(FAKE_API_SECRET, FAKE_LICENSE_KEY)
    decoded = base64.b64decode(enc).decode("utf-8")
    ciphertext_b64 = decoded.split("::")[2]
    # Should not raise
    base64.b64decode(ciphertext_b64)


def test_pbkdf2_produces_16_byte_key():
    """PBKDF2-HMAC-SHA1 with 1000 iterations and dklen=16 produces 16 bytes."""
    key = hashlib.pbkdf2_hmac(
        hash_name="sha1",
        password=FAKE_LICENSE_KEY.encode("utf-8"),
        salt=os.urandom(16),
        iterations=1000,
        dklen=16,
    )
    assert len(key) == 16


def test_pbkdf2_deterministic_with_fixed_salt():
    """Same inputs must produce the same PBKDF2 key (determinism check)."""
    fixed_salt = b"\x00" * 16
    key1 = hashlib.pbkdf2_hmac("sha1", FAKE_LICENSE_KEY.encode(), fixed_salt, 1000, 16)
    key2 = hashlib.pbkdf2_hmac("sha1", FAKE_LICENSE_KEY.encode(), fixed_salt, 1000, 16)
    assert key1 == key2


def test_encrypted_password_is_different_each_call():
    """Each call must produce a different encrypted password (random salt/IV)."""
    m = _get_module()
    enc1 = m._build_encrypted_password(FAKE_API_SECRET, FAKE_LICENSE_KEY)
    enc2 = m._build_encrypted_password(FAKE_API_SECRET, FAKE_LICENSE_KEY)
    assert enc1 != enc2


# ---------------------------------------------------------------------------
# _build_headers
# ---------------------------------------------------------------------------

def test_authorization_header_uses_basic_lowercase():
    """Authorization header must start with 'Basic ' (not 'BASIC ')."""
    m = _get_module()
    headers = m._build_headers(FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID)
    assert headers["Authorization"].startswith("Basic "), (
        f"Expected 'Basic ', got: {headers['Authorization'][:10]}"
    )


def test_accept_header_is_empty_string():
    """Accept header must be an empty string per NSE Postman collection."""
    m = _get_module()
    headers = m._build_headers(FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID)
    assert headers["Accept"] == ""


def test_referer_header_is_present():
    """Referer header must be present."""
    m = _get_module()
    headers = m._build_headers(FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID)
    assert "Referer" in headers
    assert headers["Referer"] == "www.google.com"


def test_member_id_header_is_populated():
    """memberId header must match the supplied member ID."""
    m = _get_module()
    headers = m._build_headers(FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID)
    assert headers["memberId"] == FAKE_MEMBER_ID


def test_content_type_is_json():
    m = _get_module()
    headers = m._build_headers(FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID)
    assert headers["Content-Type"] == "application/json"


def test_user_agent_matches_postman():
    m = _get_module()
    headers = m._build_headers(FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID)
    assert headers["User-Agent"] == "PostmanRuntime/7.43.0"


# ---------------------------------------------------------------------------
# get_nse_token
# ---------------------------------------------------------------------------

def test_get_nse_token_returns_basic_prefix():
    """get_nse_token() must return a string starting with 'Basic '."""
    m = _get_module()
    with patch.object(m, "settings") as s:
        s.NSE_LOGIN_USER_ID   = FAKE_USER_ID
        s.NSE_API_SECRET      = FAKE_API_SECRET
        s.NSE_API_LICENSE_KEY = FAKE_LICENSE_KEY
        s.NSE_MEMBER_ID       = FAKE_MEMBER_ID
        token = m.get_nse_token()
    assert token.startswith("Basic "), f"Expected 'Basic ', got: {token[:10]}"


def test_get_nse_token_is_available():
    """get_nse_token must be importable and callable."""
    m = _get_module()
    assert callable(m.get_nse_token)


# ---------------------------------------------------------------------------
# get_auth_headers / get_auth_headers_for_credentials
# ---------------------------------------------------------------------------

def test_get_auth_headers_returns_dict():
    m = _get_module()
    with patch.object(m, "settings") as s:
        s.NSE_LOGIN_USER_ID   = FAKE_USER_ID
        s.NSE_API_SECRET      = FAKE_API_SECRET
        s.NSE_API_LICENSE_KEY = FAKE_LICENSE_KEY
        s.NSE_MEMBER_ID       = FAKE_MEMBER_ID
        headers = m.get_auth_headers()
    assert isinstance(headers, dict)
    assert "Authorization" in headers


def test_get_auth_headers_for_credentials_returns_dict():
    m = _get_module()
    headers = m.get_auth_headers_for_credentials(
        FAKE_USER_ID, FAKE_API_SECRET, FAKE_LICENSE_KEY, FAKE_MEMBER_ID
    )
    assert isinstance(headers, dict)
    assert headers["Authorization"].startswith("Basic ")
