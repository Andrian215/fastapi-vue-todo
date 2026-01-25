from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .security import decode_token

bearer = HTTPBearer()

def get_current_user_id(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
) -> int:
    try:
        user_id = int(decode_token(creds.credentials))
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")
