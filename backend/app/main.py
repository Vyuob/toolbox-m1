from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.api.routes import auth, modules, reports, dashboard, pages, defensive
from app.core.config import settings
from app.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Toolbox Pentest",
    description="Plateforme automatisée de tests d'intrusion – Mastère Cybersécurité",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

app.include_router(pages.router)
app.include_router(auth.router,      prefix="/api/auth",      tags=["Authentification"])
app.include_router(modules.router,   prefix="/api/modules",   tags=["Modules Pentest"])
app.include_router(reports.router,   prefix="/api/reports",   tags=["Rapports"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(defensive.router, prefix="/api/defensive", tags=["SIEM Défensif"])


@app.get("/health")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
