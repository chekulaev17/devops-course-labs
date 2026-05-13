"""
This module provides routes for the reminders pages.
"""

# --------------------------------------------------------------------------------
# Imports
# --------------------------------------------------------------------------------

from app import templates
from app.utils.auth import get_storage_for_page
from app.utils.storage import ReminderStorage

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse


# --------------------------------------------------------------------------------
# Router
# --------------------------------------------------------------------------------

router = APIRouter(prefix="/reminders")


# --------------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------------

def _build_full_page_context(request: Request, storage: ReminderStorage):
  reminder_lists = storage.get_lists()
  selected_list = storage.get_selected_list()

  return {
    'request': request,
    'owner': storage.owner,
    'reminder_lists': reminder_lists,
    'selected_list': selected_list
  }


def _get_reminders_grid(request: Request, storage: ReminderStorage):
  context = _build_full_page_context(request, storage)

  return templates.TemplateResponse(
    request=request,
    name="pages/reminders.html",
    context=context
  )


# --------------------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------------------

@router.get(
  path="",
  summary="Gets the reminders page",
  tags=["Pages"],
  response_class=HTMLResponse
)
async def get_reminders(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = _build_full_page_context(request, storage)

  return templates.TemplateResponse(
    request=request,
    name="pages/reminders.html",
    context=context
  )


# --------------------------------------------------------------------------------
# Routes for list row partials
# --------------------------------------------------------------------------------

@router.get(
  path="/list-row/{list_id}",
  summary="Partial: Gets a reminder list row by ID",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_list_row(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_list = storage.get_list(list_id)
  selected_list = storage.get_selected_list()

  context = {
    'request': request,
    'reminder_list': reminder_list,
    'selected_list': selected_list
  }

  return templates.TemplateResponse(
    request=request,
    name="partials/reminders/list-row.html",
    context=context
  )


@router.delete(
  path="/list-row/{list_id}",
  summary="Partial: Deletes a reminder list row",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def delete_reminders_list_row(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  storage.delete_list(list_id)
  storage.reset_selected_after_delete(list_id)

  return _get_reminders_grid(request, storage)


@router.patch(
  path="/list-row-name/{list_id}",
  summary="Partial: Updates a reminder list row's name",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def patch_reminders_list_row_name(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  new_name: str = Form()
):
  storage.update_list_name(list_id, new_name)
  storage.set_selected_list(list_id)

  return _get_reminders_grid(request, storage)


@router.get(
  path="/list-row-edit/{list_id}",
  summary="Partial: Changes a reminder list row into editing mode",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_list_row_edit(
  list_id: int,
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  reminder_list = storage.get_list(list_id)
  selected_list = storage.get_selected_list()

  context = {
    'request': request,
    'reminder_list': reminder_list,
    'selected_list': selected_list
  }

  return templates.TemplateResponse(
    request=request,
    name="partials/reminders/list-row-edit.html",
    context=context
  )


@router.get(
  path="/new-list-row",
  summary="Partial: Gets the row for adding a new reminder list",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_new_list_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}

  return templates.TemplateResponse(
    request=request,
    name="partials/reminders/new-list-row.html",
    context=context
  )


@router.post(
  path="/new-list-row",
  summary="Partial: Creates a new reminder list",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def post_reminders_new_list_row(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page),
  reminder_list_name: str = Form()
):
  list_id = storage.create_list(reminder_list_name)
  storage.set_selected_list(list_id)

  return _get_reminders_grid(request, storage)


@router.get(
  path="/new-list-row-edit",
  summary="Partial: Changes the new reminder list row into editing mode",
  tags=["HTMX Partials"],
  response_class=HTMLResponse
)
async def get_reminders_new_list_row_edit(
  request: Request,
  storage: ReminderStorage = Depends(get_storage_for_page)
):
  context = {'request': request}

  return templates.TemplateResponse(
    request=request,
    name="partials/reminders/new-list-row-edit.html",
    context=context
  )
