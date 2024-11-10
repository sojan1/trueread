from fastapi import APIRouter, Request, HTTPException, status, Cookie
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
#from .config import SECRET_KEY, ALGORITHM  # Ensure SECRET_KEY and ALGORITHM are accessible
from config import AppConfig  # Ensure SECRET_KEY and ALGORITHM are accessible
from typing import NamedTuple

from datetime import datetime, timedelta
from fastapi_login import LoginManager

#need to be removed
ACCESS_TOKEN_EXPIRE_MINUTES = 30

manager = LoginManager(AppConfig.SECRET_KEY, token_url="/user/signin")



class UserInfo(NamedTuple):
    userid: str
    email: str

# get userinfo from token
#return error like userinfo to avoid error when token expires
#result = UserInfo(userid="error", email="Token has expired. Please log in again.")
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
        user_info = UserInfo(userid=payload.get("sub"), email=payload.get("email"))
        # request.state.user = payload
        # user_info = payload.get("sub")
        return user_info
    except ExpiredSignatureError:
        # Handle case where the token has expired
        print("Token has expired. Please log in again.")
        return {"error": "Token has expired. Please log in again."}
    except InvalidTokenError:
        # Handle case where the token is invalid
        print("Invalid token. Please provide a valid token.")
        return {"error": credentials_exception}
        #raise credentials_exception
    except Exception as e:
        # Catch any other exceptions that may occur
        print(f"An error occurred: {str(e)}")
        return {"error": "An error occurred. Please try again."}
    


# creates access token
def get_access_token(userid,email):
    expiration_time = timedelta(minutes=AppConfig.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = manager.create_access_token(
        data={"sub": userid, "email": email},  # Convert UUID to string
        expires=expiration_time)  # Pass the calculated expiration time
    return access_token