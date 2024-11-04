# routes/signin.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates

# Initialize router
router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

@router.get("/signin", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request, "active_page": "signin"})