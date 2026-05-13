"""
This module provides routes for the root pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter()


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get(
  path="/",
  summary="Redirects to reminders",
  tags=["Pages"]
)
async def get_root():
  return RedirectResponse("/login")


@router.get(
  path="/404",
  summary="Gets the not found page",
  tags=["Pages"],
  response_class=HTMLResponse
)
async def get_not_found(request: Request):
  context = {
    'request': request
  }

  return templates.TemplateResponse(
    request=request,
    name="pages/not-found.html",
    context=context
  )
