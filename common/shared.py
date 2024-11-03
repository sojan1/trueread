from fastapi import Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Initialize Jinja2Templates once, with caching disabled
templates = Jinja2Templates(directory="templates")
templates.env.cache = {}

# Export commonly used dependencies
Req= Request
Frm = Form
HTMLRes = HTMLResponse