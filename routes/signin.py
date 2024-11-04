# routes/signin.py
from fastapi import APIRouter, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse
from common.shared import templates

from fastapi_login import LoginManager
import bcrypt

# Initialize router
router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

#secretkey to generate token
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"  # You can choose other algorithms as needed
manager = LoginManager(SECRET_KEY, token_url="/user/signin")


#dummydb
fake_users_db = {
    "sojan@gmail.com": {
        "email": "sojan@gmail.com",
        "password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        "userid": "sojanct"  # Adding a user ID
    }
}

@router.get("/signin", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "active_page": "signin"})

@router.post("/user/signin")
def login(email: str = Form(...), password: str = Form(...), response: Response = None):

    user = load_user(email)
    if not user or not verify_password(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = manager.create_access_token(data={"sub": email})
    #return RedirectResponse(url=f"/success?token={access_token}")
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