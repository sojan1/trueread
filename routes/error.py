# routes/error.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes
# from fastapi.templating import Jinja2Templates

# Initialize router
router = APIRouter()

templates.env.cache = {}  # Disable caching if needed

# Define the /help route
@router.get("/error", response_class=HTMLResponse)
async def read_error(request: Request):
    return templates.TemplateResponse("error.html", {"request": request, "active_page": "error","error":"Error Template"}})