import base64
import secrets
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from config import settings


def _build_encrypted_password(api_secret: str, license_key: str) -> str:
    """
    NSE spec:
      salt              = random 32-char hex  e.g. 9A1c74744b944d9bd34e7de3a964fb19
      iv                = random 32-char hex  e.g. 90E9c0485bc76e864e5aae05a34d356f
      plain_text        = api_secret|<random_number>
      aes_encrypted_val = AES-128-CBC(key=bytes.fromhex(license_key[:32]), iv=bytes.fromhex(iv), plain_text)
      Encrypted Password = base64(iv::salt::aes_encrypted_val)
    """
    salt = secrets.token_hex(16)                                    # 32-char hex
    iv   = secrets.token_hex(16)                                    # 32-char hex
    random_number = secrets.randbelow(89999999999) + 10000000000    # 11-digit number

    plain_text = f"{api_secret}|{random_number}"
    key      = bytes.fromhex(license_key)   # 32-char hex → 16 bytes for AES-128
    iv_bytes = bytes.fromhex(iv)            # 32-char hex → 16 bytes for AES IV

    cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
    aes_encrypted_val = base64.b64encode(
        cipher.encrypt(pad(plain_text.encode("utf-8"), AES.block_size))
    ).decode("utf-8")

    combined = f"{iv}::{salt}::{aes_encrypted_val}"
    return base64.b64encode(combined.encode("utf-8")).decode("utf-8")


def _build_headers(user_id: str, api_secret: str, license_key: str, member_id: str) -> dict:
    """
    NSE required request headers per spec:
      Content-Type  : application/json
      memberId      : Member Code registered with NSE  (INT in spec, sent as string)
      Authorization : BASIC base64(login_user_id:encrypted_password)

    Extra connection headers required to prevent gateway timeout:
      User-Agent, Accept, Accept-Language, Connection
    """
    encrypted_password = _build_encrypted_password(api_secret, license_key)
    credentials  = f"{user_id}:{encrypted_password}"
    authorization = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

    return {
        "Content-Type":   "application/json",
        "memberId":       str(member_id),
        "Authorization":  f"BASIC {authorization}",
        "User-Agent":     "PostmanRuntime/7.43.0",
        "Accept":         "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection":     "keep-alive",
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
        settings.NSE_API_LICENSE_KEY
    )
    credentials = f"{settings.NSE_LOGIN_USER_ID}:{encrypted_password}"
    authorization = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    return f"BASIC {authorization}"


def get_auth_headers_for_credentials(
    user_id: str,
    api_secret: str,
    license_key: str,
    member_id: str,
) -> dict:
    """Build headers from caller-supplied credentials — used by the login endpoint."""
    return _build_headers(user_id, api_secret, license_key, member_id)
