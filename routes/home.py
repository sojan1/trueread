# routes/home.py
from fastapi import APIRouter, Request, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse
from common.shared import templates
from fastapi_login import LoginManager
import jwt
from jwt.exceptions import InvalidTokenError
from colorama import Fore, Style, init

# Initialize router
router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

#secretkey to generate token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"  # You can choose other algorithms as needed
manager = LoginManager(SECRET_KEY, token_url="/user/signin")


# Define the /help route
@router.get("/help", response_class=HTMLResponse)
async def read_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request, "active_page": "help"})

@router.get("/home")
def protected_home(request: Request, access_token: str = Cookie(None)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},)
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        request.state.user = payload
        username: str = payload.get("sub")

        # request.state.user = payload
        # user_info = getattr(request.state, "user", None)
        # print(str(user_info))

    except InvalidTokenError:
        raise credentials_exception
    
    return templates.TemplateResponse("home.html", {"request": request, "active_page": "home", "user": username})
    # Optionally, you can return something as well
    #return {"access_token": f"{username} - {access_token}"}