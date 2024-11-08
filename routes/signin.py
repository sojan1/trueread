# routes/signin.py
from fastapi import APIRouter, Request, Form, HTTPException, Response, Depends
from fastapi.responses import HTMLResponse
from common.shared import templates
from sqlalchemy.orm import Session
from database import engine, Base #,SessionLocal
from fastapi_async_sqlalchemy import db
from sqlalchemy import select  # Import select from sqlalchemy

from fastapi_login import LoginManager
import bcrypt

#Base.metadata.create_all(bind=engine)

# Initialize router
router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


#secretkey to generate token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"  # You can choose other algorithms as needed
manager = LoginManager(SECRET_KEY, token_url="/user/signin")
from database import User  # Import User model from database.py

# #dummydb
# fake_users_db = {
#     "sojan@gmail.com": {
#         "email": "sojan@gmail.com",
#         "password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
#         "userid": "sojanct"  # Adding a user ID
#     }
# }

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
    
    #page is redirected using ajax in signin page to /home
    access_token = manager.create_access_token(data={"sub": email})
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True)
    return {"access_token": access_token}


@manager.user_loader
def get_user(email: str):
    return load_user(email)

#functions
def load_user(email: str):
    return fake_users_db.get(email)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))