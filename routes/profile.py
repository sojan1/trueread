# routes/profile.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# Define the /profile route
@router.get("/profile", response_class=HTMLResponse)
async def read_profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request, "active_page": "profile"})