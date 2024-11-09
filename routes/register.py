# routes/signup.py
from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from common.shared import templates
import bcrypt
from fastapi_async_sqlalchemy import db
from database import User
from typing import Optional

from database import User
#from utils import add_to_database

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
    displayname: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    name: str = Form(...),
    email: str = Form(...),
    phone: Optional[str] = Form(None)
):
    
    if password != confirm_password:
        return render_template(
            "register.html",
            request,
            context={"displayname": displayname, "name": name, "email": email, "phone": phone},
            error="Passwords do not match"
        )
        
        #raise HTTPException(status_code=400, detail="Passwords do not match")

        
    
    new_user = User(displayname=displayname, password=password, name=name, email=email, phone=phone)
    new_user.password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    try:
        # Use the session from SQLAlchemyMiddleware
        async with db():
            db.session.add(new_user)  # Add the new user to the session
            await db.session.commit()  # Commit the session to save the new user
        
        # Redirect to success page if successful
        return render_template("signupsuccess.html", request, context={"user": new_user})
    except HTTPException as e:
        # Handle specific HTTP exceptions if they occur
        return render_template(
            "register.html",
            request,
            context={"displayname": displayname, "name": name, "email": email, "phone": phone},
            error=e.detail
        )
    except Exception as e:
        # Handle other exceptions (e.g., database errors)
        return render_template(
            "register.html",
            request,
            context={"displayname": displayname, "name": name, "email": email, "phone": phone},
            error=str(e)  # Show the error message
        )
    # try:
    #     add_to_database(new_user)
    #     # Redirect to success page if successful
    #     return render_template("signupsuccess.html", request, context={"user": new_user})
    # except HTTPException as e:
    #     # Redirect back with error message and pre-filled data in case of exception
    #     return render_template(
    #         "register.html",
    #         request,
    #         context={"displayname": displayname, "name": name, "email": email, "phone": phone},
    #         error=e.detail
    #     )


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