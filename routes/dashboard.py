# routes/dashboard.py
from fastapi import APIRouter, Request, HTTPException, status, Cookie
from fastapi.responses import HTMLResponse
from common.shared import templates
from colorama import Fore, Style, init
from auth import get_current_user 

# from fastapi_login import LoginManager
# import jwt
# from jwt.exceptions import InvalidTokenError


# Initialize router
router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# Define the /help route
@router.get("/help", response_class=HTMLResponse)
async def read_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request, "active_page": "help"})

@router.get("/dashboard")
def protected_home(request: Request, access_token: str = Cookie(None)):
    user_info = get_current_user(request, access_token)  # Use get_current_user for authentication
    return templates.TemplateResponse("dashboard.html", {"request": request, "active_page": "home", "user": user_info})
    # Optionally, you can return something as well
    #return {"access_token": f"{username} - {access_token}"}
