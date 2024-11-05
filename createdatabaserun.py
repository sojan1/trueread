#-main.py
##-HeadersBegin
###-HtmlBegin
from fastapi import FastAPI,Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn

# Serve static files from the 'static' directory , without StaticFiles CSS will not work[Error:'Internal Server Error']
from fastapi.staticfiles import StaticFiles 

from createdatabase import SessionLocal, User  # Import from database.py
from sqlalchemy.exc import IntegrityError



app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Serve static files from the 'static' directory , without this CSS will not work, and it will display error as 'Internal Server Error'
app.mount("/static", StaticFiles(directory="static"), name="static")

