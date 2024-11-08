# routes/logout.py
from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

# Define the /logout route
@router.get("/logout", response_class=HTMLResponse)
async def read_did(response: Response,request: Request):
    response.set_cookie(key="access_token", value="", expires=0, httponly=True, secure=True)

    #response.set_cookie(key="access_token", value="", httponly=True, secure=True)
    #response.delete_cookie(key="access_token")
    #return {"message": "Logged out successfully"}
    return templates.TemplateResponse("logout.html", {"request": request, "active_page": "logout","message": "Logged out successfully"})