#-main.py
from fastapi import FastAPI,Form, HTTPException, Request, Depends, status, Response, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from colorama import Fore, Style, init
import jwt
from jwt.exceptions import InvalidTokenError


from routes import help  # Import the help module
from routes import signin # Import the signin module
from routes import register # Import the register module
from routes import home # Import the home module

#to use shared headers, 
# purpose is to use route, route allows to use prefix in subfolders
#from routes import help
#router = APIRouter(prefix="/help") 

import uvicorn
from template_utils import render_template  # Import the utility function

# Serve static files from the 'static' directory , without StaticFiles CSS will not work[Error:'Internal Server Error']
from fastapi.staticfiles import StaticFiles 
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_login.exceptions import InvalidCredentialsException
import bcrypt


from fastapi_sqlalchemy import DBSessionMiddleware
from database import DATABASE_URL

from fastapi_async_sqlalchemy import SQLAlchemyMiddleware
from fastapi_async_sqlalchemy import db  # provide access to a database session
from sqlalchemy import column
from sqlalchemy import table

# from sqlalchemy.exc import IntegrityError
# from database import DATABASE_URL, User, Base
# from utils import add_to_database
##-HeadersEnd


app = FastAPI()
templates = Jinja2Templates(directory="templates")
templates.env.cache = {}  # Disable caching

# Serve static files from the 'static' directory , without this CSS will not work, and it will display error as 'Internal Server Error'
app.mount("/static", StaticFiles(directory="static"), name="static")

# fastapiSqlalchemy -  not used
#app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)

app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=DATABASE_URL,  # Use the async connection string here
    engine_args={
        "echo": True,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    },
)

app.include_router(help.router)
app.include_router(signin.router)
app.include_router(register.router)
app.include_router(home.router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

print(Style.BRIGHT + Fore.RED + "This is a bold error message.")
print(Style.RESET_ALL)


# @app.get("/home", response_class=HTMLResponse)
# def read_home(user=Depends(verify_token)):
#     return HTMLResponse("<h1>Welcome to the protected home page!</h1>")

# @app.get("/home", response_class=HTMLResponse)
# async def read_home(request: Request, token: str = Depends(verify_token)):
#     return templates.TemplateResponse("home.html", {"request": request, "active_page": "home"})