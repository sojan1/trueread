# routes/did.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# Define the /did route
@router.get("/did", response_class=HTMLResponse)
async def read_did(request: Request):
    return templates.TemplateResponse("did.html", {"request": request, "active_page": "did"})