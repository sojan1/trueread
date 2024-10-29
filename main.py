#-main.py
##-HeadersBegin
###-HtmlBegin
from fastapi import FastAPI,Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from template_utils import render_template  # Import the utility function
# Serve static files from the 'static' directory , without StaticFiles CSS will not work[Error:'Internal Server Error']
from fastapi.staticfiles import StaticFiles 
###-HtmlEnds


#sample - can be removed
#from database import SessionLocal, User  # Import from database.py

from fastapi_sqlalchemy import DBSessionMiddleware, db
from database import DATABASE_URL, User, Base
from sqlalchemy.exc import IntegrityError
from utils import add_to_database
##-HeadersEnd


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Serve static files from the 'static' directory , without this CSS will not work, and it will display error as 'Internal Server Error'
app.mount("/static", StaticFiles(directory="static"), name="static")

# fastapiSqlalchemy
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def login(request: Request):
    return render_template("register.html", request)
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

    
