# routes/signup.py
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from common.shared import templates

from fastapi_sqlalchemy import DBSessionMiddleware, db
from database import DATABASE_URL, User, Base
from sqlalchemy.exc import IntegrityError
from utils import add_to_database

# Initialize router
router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

@router.get("/signupsuccess", response_class=HTMLResponse)
async def success_page(request: Request, token: str = None):
    return templates.TemplateResponse("signinsuccess.html", {"request": request, "token": token})


@router.get("/register", response_class=HTMLResponse)
async def login(request: Request):
    return render_template("register.html", request, active_page="register")  # Set active_page for the register page
    #return templates.TemplateResponse("register.html", {"request": request})



@router.post("/register")
async def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: str = Form(...)
):
    if password != confirm_password:
        return render_template(
            "register.html",
            request,
            context={"username": username, "name": name, "email": email, "phone": phone},
            error="Passwords do not match"
        )
        #raise HTTPException(status_code=400, detail="Passwords do not match")
    
    new_user = User(username=username, password=password, name=name, email=email, phone=phone)
    try:
        add_to_database(new_user)
        # Redirect to success page if successful
        return render_template("signupsuccess.html", request, context={"user": new_user})
    except HTTPException as e:
        # Redirect back with error message and pre-filled data in case of exception
        return render_template(
            "register.html",
            request,
            context={"username": username, "name": name, "email": email, "phone": phone},
            error=e.detail
        )


def render_template(
    template_name: str,
    request: Request,
    context: dict = {},
    error: str = None,
    active_page: str = None  # New parameter for the active sidebar link
):
    """
    Renders a template with optional error handling and data preservation.
    """
    # Add request, error, and active_page to context for use in the template
    context.update({"request": request})
    if error:
        context.update({"error": error})
    if active_page:
        context.update({"active_page": active_page})  # Add active_page to context
    return templates.TemplateResponse(template_name, context)