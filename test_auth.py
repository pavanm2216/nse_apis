from auth.nse_auth import get_auth_headers

headers = get_auth_headers()
print("Headers generated successfully:")
for k, v in headers.items():
    print(f"  {k}: {v[:60]}...")
