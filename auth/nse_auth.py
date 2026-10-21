import base64
import hashlib
import os
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from config import settings


def _build_encrypted_password(api_secret: str, license_key: str) -> str:
    """
    NSE Postman pre-request script algorithm:
      1. Generate random 16-byte salt and 16-byte IV
      2. random_number = random int 1..10,000,000,000
      3. plain_text = api_secret|random_number
      4. key = PBKDF2-HMAC-SHA1(password=license_key.encode(), salt=salt, iterations=1000, dklen=16)
      5. aes_encrypted_val = base64(AES-128-CBC(key, iv, PKCS7(plain_text)))
      6. combined = iv_hex::salt_hex::aes_encrypted_val
      7. encrypted_password = base64(combined)
    """
    salt_bytes = os.urandom(16)
    iv_bytes   = os.urandom(16)
    random_number = secrets.randbelow(10_000_000_000) + 1  # 1..10,000,000,000

    plain_text = f"{api_secret}|{random_number}"

    key = hashlib.pbkdf2_hmac(
        hash_name="sha1",
        password=license_key.encode("utf-8"),
        salt=salt_bytes,
        iterations=1000,
        dklen=16,
    )

    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    aes_encrypted_val = base64.b64encode(
        cipher.encrypt(pad(plain_text.encode("utf-8"), AES.block_size))
    ).decode("utf-8")

    iv_hex   = iv_bytes.hex()
    salt_hex = salt_bytes.hex()
    combined = f"{iv_hex}::{salt_hex}::{aes_encrypted_val}"
    return base64.b64encode(combined.encode("utf-8")).decode("utf-8")


def _build_headers(user_id: str, api_secret: str, license_key: str, member_id: str) -> dict:
    """
    NSE required request headers matching the official Postman collection:
      Content-Type   : application/json
      memberId       : NSE member ID
      Authorization  : Basic base64(login_user_id:encrypted_password)
      User-Agent     : PostmanRuntime/7.43.0
      Accept         : (empty string)
      Accept-Language: en-US
      Connection     : keep-alive
      Referer        : www.google.com
    """
    encrypted_password = _build_encrypted_password(api_secret, license_key)
    credentials   = f"{user_id}:{encrypted_password}"
    authorization = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    return {
        "Content-Type":    "application/json",
        "memberId":        str(member_id),
        "Authorization":   f"Basic {authorization}",
        "User-Agent":      "PostmanRuntime/7.43.0",
        "Accept":          "",
        "Accept-Language": "en-US",
        "Connection":      "keep-alive",
        "Referer":         "www.google.com",
    }


def get_auth_headers() -> dict:
    """Build headers from .env credentials — used by all existing routers."""
    return _build_headers(
        user_id=settings.NSE_LOGIN_USER_ID,
        api_secret=settings.NSE_API_SECRET,
        license_key=settings.NSE_API_LICENSE_KEY,
        member_id=settings.NSE_MEMBER_ID,
    )


def get_nse_token() -> str:
    """Return just the NSE Authorization header value — used as the token in login response."""
    encrypted_password = _build_encrypted_password(
        settings.NSE_API_SECRET,
        settings.NSE_API_LICENSE_KEY,
    )
    credentials   = f"{settings.NSE_LOGIN_USER_ID}:{encrypted_password}"
    authorization = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return f"Basic {authorization}"


def get_auth_headers_for_credentials(
    user_id: str,
    api_secret: str,
    license_key: str,
    member_id: str,
) -> dict:
    """Build headers from caller-supplied credentials — used by the login endpoint."""
    return _build_headers(user_id, api_secret, license_key, member_id)
