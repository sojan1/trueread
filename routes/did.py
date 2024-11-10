# routes/did.py
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from common.shared import templates, Req, HTMLRes

from pydantic import BaseModel

router = APIRouter()
templates.env.cache = {}  # Disable caching if needed

class DIDRequest(BaseModel):
    name: str
    email: str
    identityType: str

# Define the /did route
@router.get("/did", response_class=HTMLResponse)
async def read_did(request: Request):
    return templates.TemplateResponse("did.html", {"request": request, "active_page": "did"})

@router.post("/did")
async def create_did(request: DIDRequest):
    # Extract data from the request
    name = request.name + "sojan"
    email = request.email
    identity_type = request.identityType
    
    # Here you can process or store the data as needed
    # Let's assume DID creation was successful for this example

    # Create a response
    response = {
        "status": "success",
        "message": "DID created successfully",
        "data": {
            "name": name+"##########Sojan*********",
            "email": email,
            "identityType": identity_type
        }
    }
    return response