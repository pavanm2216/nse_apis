"""Run only mocked suites with dummy settings; never load live credentials."""
import os
from pathlib import Path
import socket
import sys

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))
os.environ.update(
    NSE_LOGIN_USER_ID="offline-user",
    NSE_API_SECRET="offline-secret",
    NSE_API_LICENSE_KEY="0123456789abcdef0123456789abcdef",
    NSE_MEMBER_ID="1003338",  # Existing header test's expected fixture value.
    NSE_MEMBER_CODE="offline-member",
    NSE_BASE_URL="https://nse.invalid",
    NSE_PROXY="",
    APP_USERNAME="offline-user",
    APP_PASSWORD="offline-password",
    JWT_SECRET="offline-testing-key-with-at-least-32-characters",
    DB_USER="offline",
    DB_PASSWORD="offline",
    DB_HOST="127.0.0.1",
    DB_PORT="5432",
    DB_NAME="offline",
    DB_SSL="false",
    DATABASE_URL="postgresql+asyncpg://offline:offline@127.0.0.1:5432/offline",
)

# Windows asyncio uses a loopback socket pair internally. Permit that while
# blocking external connections; all application HTTP/database calls are mocked.
_connect = socket.socket.connect
_connect_ex = socket.socket.connect_ex


def _guard(method):
    def guarded(sock, address):
        if isinstance(address, tuple) and address[0] in ("127.0.0.1", "::1"):
            return method(sock, address)
        raise RuntimeError("External network blocked during offline tests")
    return guarded


if __name__ == "__main__":
    socket.socket.connect = _guard(_connect)
    socket.socket.connect_ex = _guard(_connect_ex)
    import pytest

    # Explicit files avoid collecting legacy tests that call external servers.
    sys.exit(pytest.main([
        "test_auth_headers.py", "tests/test_nse_spec_contract.py",
        "-q", "--tb=short", "--disable-warnings",
    ]))
