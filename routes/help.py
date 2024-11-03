#loaded from the common/shared.py
from fastapi import APIRouter, Depends
from common.shared import templates, Req, HTMLRes

router = APIRouter(prefix="/help")  # Define routes with a common prefix

@router.get("/help", response_class=HTMLRes)
async def read_root(request: Req):
    return templates.TemplateResponse("help.html", {"request": request, "active_page": "help"})