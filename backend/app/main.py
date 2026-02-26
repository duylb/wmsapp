from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.core.rate_limit import limiter, rate_limit_exceeded_handler
from app.database.init_db import init_db

from app.routers import (
    auth,
    users,
    companies,
    staff,
    roster,
    payroll,
    shifts,
    subscription,
    billing,
    super_admin,
    websocket,
)

app = FastAPI(title=settings.APP_NAME)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(users.router, prefix=settings.API_PREFIX)
app.include_router(companies.router, prefix=settings.API_PREFIX)
app.include_router(staff.router, prefix=settings.API_PREFIX)
app.include_router(roster.router, prefix=settings.API_PREFIX)
app.include_router(payroll.router, prefix=settings.API_PREFIX)
app.include_router(shifts.router, prefix=settings.API_PREFIX)
app.include_router(subscription.router, prefix=settings.API_PREFIX)
app.include_router(billing.router, prefix=settings.API_PREFIX)
app.include_router(super_admin.router, prefix=settings.API_PREFIX)
app.include_router(websocket.router)

@app.get("/")
def root():
    return {"status": "ok"}