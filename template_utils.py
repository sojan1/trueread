# template_utils.py
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

def render_template(
    template_name: str,
    request: Request,
    context: dict = {},
    error: str = None
):
    """
    Renders a template with optional error handling and data preservation.
    """
    # Add request and error to context for use in the template
    context.update({"request": request})
    if error:
        context.update({"error": error})
    return templates.TemplateResponse(template_name, context)
