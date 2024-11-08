# routes/signin.py
from fastapi import APIRouter, Request, Form, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse
from common.shared import templates
from sqlalchemy.orm import Session
from database import engine, Base #,SessionLocal
from fastapi_async_sqlalchemy import db
from sqlalchemy import select  # Import select from sqlalchemy
from database import User  # Import User model from database.py


from fastapi_login import LoginManager
import bcrypt
from auth import get_access_token 

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed


@router.get("/signin", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "active_page": "signin"})

@router.post("/user/signin")
async def login(
    response: Response,
    email: str = Form(...),
    password: str = Form(...)
):
    async with db():
        # Use select from sqlalchemy to create the query
        stmt = select(User).where(User.email == email)
        result = await db.session.execute(stmt)
        user = result.scalar_one_or_none()  # Get the user or None

    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token=get_access_token(str(user.id),user.email);
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return {"access_token": access_token}

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))