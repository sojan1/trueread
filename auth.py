from fastapi import APIRouter, Request, HTTPException, status, Cookie
import jwt
from jwt.exceptions import InvalidTokenError
#from .config import SECRET_KEY, ALGORITHM  # Ensure SECRET_KEY and ALGORITHM are accessible
from config import AppConfig  # Ensure SECRET_KEY and ALGORITHM are accessible
def get_current_user(request: Request, access_token: str = Cookie(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, AppConfig.SECRET_KEY, algorithms=[AppConfig.ALGORITHM])
        request.state.user = payload
        user_info = payload.get("sub")
        return user_info
    except InvalidTokenError:
        raise credentials_exception
    # except jwt.ExpiredSignatureError:
    #     # Handle token expiration
    #     return None
    # except jwt.InvalidTokenError:
    #     # Handle invalid token
    #     return None

