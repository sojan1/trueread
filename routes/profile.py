# routes/profile.py
from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes

from sqlalchemy.orm import Session
from database import engine, Base #,SessionLocal
from fastapi_async_sqlalchemy import db
from sqlalchemy import select  # Import select from sqlalchemy
from database import User  # Import User model from database.py

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# Define the /profile route
@router.get("/profile", response_class=HTMLResponse)
async def read_profile(request: Request):
        # Query multiple fields from the database
    #user = await db.query(User).first()  # Get the first user as an example

        # Create the context dictionary, including user and active page
        # context = {
        #     "request": request,        # Required for TemplateResponse
        #     "active_page": "profile",  # For the active page indicator
        #     "user": user               # The user data from the database
        # }
        #return templates.TemplateResponse("profile.html", context)
    async with db():
        # Use select from sqlalchemy to create the query
        stmt = select(User).where(User.email == 'sojan@gmail.com')
        result = await db.session.execute(stmt)
        user = result.scalar_one_or_none()  # Get the user or None

        context = {
        "request": request,
        "active_page": "profile",
        "user": user
    }
        print(context)
    return templates.TemplateResponse("profile.html", context)
    #return templates.TemplateResponse("profile.html", {"request": request, "active_page": "profile"})