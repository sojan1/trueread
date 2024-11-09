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


# async def exec(email):
#     async with db():
#         # Use select from sqlalchemy to create the query
#         stmt = select(User).where(User.email == email)
#         result = await db.session.execute(stmt)
#         user = result.scalar_one_or_none()  # Get the user or None
#         return user
 

# Define the /profile route
@router.get("/profile", response_class=HTMLResponse)

#async def read_profile(request: Request):
async def read_profile(request: Request, access_token: str = Cookie(None)):
    user_info_auth = get_current_user(request, access_token) 

    user = await profile_query(user_info_auth.email);

    # async with db():
    #     # Use select from sqlalchemy to create the query
    #     stmt = select(User).where(User.email == user_info_auth.email)
    #     result = await db.session.execute(stmt)
    #     user = result.scalar_one_or_none()  # Get the user or None
        


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
    #async with db():
    # stmt = update(User).where(User.email == user_info_auth.email).values(phone=phone)
    # result = await db.session.execute(stmt)
    # await db.session.commit()

    await profile_command(user_info_auth.email,phone)

    # Use select from sqlalchemy to create the query
    stmt = select(User).where(User.email == user_info_auth.email)
    result = await db.session.execute(stmt)
    user = result.scalar_one_or_none()  # Get the user or None
        

    context = {
        "request": request,
        "active_page": "profile",
        "user": user
        }

    #return "updated"
    return templates.TemplateResponse("profile.html", context)




