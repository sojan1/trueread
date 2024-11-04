# routes/help.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes
# from fastapi.templating import Jinja2Templates

# Initialize router
router = APIRouter()

# Define templates directory as the root folder
#templates = Jinja2Templates(directory="./templates")
templates.env.cache = {}  # Disable caching if needed

# Define the /help route
@router.get("/help", response_class=HTMLResponse)
async def read_help(request: Request):
    return templates.TemplateResponse("help.html", {"request": request, "active_page": "help"})


# #loaded from the common/shared.py
# from fastapi import APIRouter, Depends
# from common.shared import templates, Req, HTMLRes

# router = APIRouter(prefix="/help")  # Define routes with a common prefix

# @router.get("/help", response_class=HTMLRes)
# async def read_root(request: Req):
#     return templates.TemplateResponse("help.html", {"request": request, "active_page": "help"})