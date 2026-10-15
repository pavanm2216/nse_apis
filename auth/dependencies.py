from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from config import settings

bearer_scheme = HTTPBearer()


def require_auth(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """Validates the JWT signature and expiry on every protected request."""
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing authorization token")
    try:
        jwt.decode(credentials.credentials, settings.JWT_SECRET, algorithms=["HS256"])
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return credentials.credentials
