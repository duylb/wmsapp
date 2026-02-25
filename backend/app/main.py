from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.init_db import init_db

from app.routers import (
    auth,
    companies,
    users,
    staff,
    shifts,
    roster,
    payroll,
)

# ---------------------------------------------------
# APP INIT
# ---------------------------------------------------

app = FastAPI(
    title="RosMan WMS API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ---------------------------------------------------
# CORS
# ---------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------
# STARTUP EVENT
# ---------------------------------------------------

@app.on_event("startup")
def on_startup():
    init_db()

# ---------------------------------------------------
# HEALTH CHECK
# ---------------------------------------------------

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}

# ---------------------------------------------------
# API ROUTES
# ---------------------------------------------------

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=f"{API_PREFIX}/auth", tags=["Auth"])
app.include_router(companies.router, prefix=f"{API_PREFIX}/companies", tags=["Companies"])
app.include_router(users.router, prefix=f"{API_PREFIX}/users", tags=["Users"])
app.include_router(staff.router, prefix=f"{API_PREFIX}/staff", tags=["Staff"])
app.include_router(shifts.router, prefix=f"{API_PREFIX}/shifts", tags=["Shifts"])
app.include_router(roster.router, prefix=f"{API_PREFIX}/roster", tags=["Roster"])
app.include_router(payroll.router, prefix=f"{API_PREFIX}/payroll", tags=["Payroll"])