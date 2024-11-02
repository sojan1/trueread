#-main.py
from fastapi import FastAPI,Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from template_utils import render_template  # Import the utility function

# Serve static files from the 'static' directory , without StaticFiles CSS will not work[Error:'Internal Server Error']
from fastapi.staticfiles import StaticFiles 
from fastapi_login import LoginManager
import bcrypt


#sample - can be removed
#from database import SessionLocal, User  # Import from database.py

from fastapi_sqlalchemy import DBSessionMiddleware, db
from database import DATABASE_URL, User, Base
from sqlalchemy.exc import IntegrityError
from utils import add_to_database
##-HeadersEnd


app = FastAPI()
templates = Jinja2Templates(directory="templates")

#secretkey to generate token
SECRET_KEY = "your_secret_key"
manager = LoginManager(SECRET_KEY, token_url="/user/signin")

#dummydb
fake_users_db = {
    "sojan@gmail.com": {
        "email": "sojan@gmail.com",
        "password": bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    }
}

#functions
def load_user(email: str):
    return fake_users_db.get(email)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


@app.post("/user/signin")
def login(email: str = Form(...), password: str = Form(...)):
    user = load_user(email)
    if not user or not verify_password(password, user['password']):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = manager.create_access_token(data={"sub": email})
    #return RedirectResponse(url=f"/success?token={access_token}")
    return {"access_token": access_token}


@manager.user_loader
def get_user(email: str):
    return load_user(email)

@app.get("/signin", response_class=HTMLResponse)
async def sign_in_page(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})


@app.get("/success", response_class=HTMLResponse)
async def success_page(request: Request, token: str = None):
    return templates.TemplateResponse("signinsuccess.html", {"request": request, "token": token})






# Serve static files from the 'static' directory , without this CSS will not work, and it will display error as 'Internal Server Error'
app.mount("/static", StaticFiles(directory="static"), name="static")

# fastapiSqlalchemy
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "active_page": "login"})

@app.get("/home", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "active_page": "home"})

@app.get("/help", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("help.html", {"request": request, "active_page": "help"})









@app.get("/register", response_class=HTMLResponse)
async def login(request: Request):
    return render_template("register.html", request, active_page="register")  # Set active_page for the register page
    #return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
):
    if password != confirm_password:
        return render_template(
            "register.html",
            request,
            context={"username": username, "name": name, "email": email, "phone": phone},
            error="Passwords do not match"
        )
        #raise HTTPException(status_code=400, detail="Passwords do not match")
    
    new_user = User(username=username, password=password, name=name, email=email, phone=phone)
    try:
        add_to_database(new_user)
        # Redirect to success page if successful
        return render_template("success.html", request, context={"user": new_user})
    except HTTPException as e:
        # Redirect back with error message and pre-filled data in case of exception
        return render_template(
            "register.html",
            request,
            context={"username": username, "name": name, "email": email, "phone": phone},
            error=e.detail
        )

    
