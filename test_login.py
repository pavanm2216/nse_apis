import getpass
import httpx

username = input("Username: ")
password = getpass.getpass("Password: ")

try:
    response = httpx.post(
        "http://127.0.0.1:8000/api/v1/auth/login",
        json={"username": username, "password": password},
        timeout=15,
    )
    data = response.json()
    token = data.get("access_token") or ""

    print("HTTP Status:", response.status_code)
    print("Token Type:", data.get("token_type"))
    print("JWT Format:", len(token.split(".")) == 3)
    print("Message:", data.get("message"))
except Exception as exc:
    print("Test failed:", type(exc).__name__)
