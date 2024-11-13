# routes/profile.py
from fastapi import APIRouter, Request, Depends, Cookie, Form, HTTPException
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes

from sqlalchemy.orm import Session
from database import engine, Base #,SessionLocal
from sqlalchemy import select, update, insert, delete  # Import select from sqlalchemy
# Import User model from database.py
from database_execute_async import profile_query, profile_command

from fastapi_async_sqlalchemy import db
from database import User
from typing import Optional

from auth import get_current_user 

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed
 

# Define the /profile route
@router.get("/profile", response_class=HTMLResponse)

#async def read_profile(request: Request):
async def read_profile(request: Request, access_token: str = Cookie(None)):

    user_info_auth = get_current_user(request, access_token) 
    print(user_info_auth)
    user = await profile_query(user_info_auth.email);

    context = {
        "request": request,
        "active_page": "profile",
        "user": user
    }
    #print(context)
    return templates.TemplateResponse("profile.html", context)
    #return templates.TemplateResponse("profile.html", {"request": request, "active_page": "profile"})




@router.post("/profile", response_class=HTMLResponse)
async def edit_profile(
    request: Request,
    phone: Optional[str] = Form(None), access_token: str = Cookie(None)
):
    user_info_auth = get_current_user(request, access_token) 

    await profile_command(user_info_auth.email,phone)
    user = await profile_query(user_info_auth.email);

    context = {
        "request": request,
        "active_page": "profile",
        "user": user
        }

    #return "updated"
    return templates.TemplateResponse("profile.html", context)




