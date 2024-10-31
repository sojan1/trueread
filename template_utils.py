# template_utils.py
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="templates")

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
