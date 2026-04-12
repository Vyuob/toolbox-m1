from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="frontend/templates")


@router.get("/", response_class=RedirectResponse, include_in_schema=False)
def root():
    return RedirectResponse(url="/login")


@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@router.get("/modules", response_class=HTMLResponse, include_in_schema=False)
def modules_page(request: Request):
    return templates.TemplateResponse("modules.html", {"request": request})


@router.get("/reports", response_class=HTMLResponse, include_in_schema=False)
def reports_page(request: Request):
    return templates.TemplateResponse("reports.html", {"request": request})


@router.get("/siem", response_class=HTMLResponse, include_in_schema=False)
def siem_page(request: Request):
    return templates.TemplateResponse("siem.html", {"request": request})
