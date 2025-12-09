"""
Life OS Backend - FastAPI Application
Main entry point for the Life OS API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import otto as otto_router
from tax import routers as tax_router
from audio import routers as audio_router
from otto_runs import router as otto_runs_router
from otto_tasks import router as otto_tasks_router
from life_os_tasks import router as life_os_tasks_router
from bills import router as bills_router
from calendar_api import router as calendar_router
from income import router as income_router
from transactions import router as transactions_router
from categories import router as categories_router
from otto_memory import router as otto_memory_router
from activity_reporting import router as activity_reporting_router
from database import init_db

app = FastAPI(
    title="Life OS API",
    description="Household management and personal automation API",
    version="0.1.0"
)

# CORS configuration - allow from localhost and local network
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow from anywhere (localhost, local network, phone, etc.)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Include routers
app.include_router(otto_router.router)
app.include_router(otto_runs_router)
app.include_router(otto_tasks_router)
app.include_router(life_os_tasks_router)
app.include_router(bills_router)
app.include_router(calendar_router)
app.include_router(income_router)
app.include_router(transactions_router)
app.include_router(categories_router)
app.include_router(otto_memory_router)
app.include_router(activity_reporting_router)
app.include_router(tax_router.router)
app.include_router(audio_router.router)

@app.get("/")
async def root():
    return {"message": "Life OS API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

# TODO: Add routes for:
# - Tasks (kanban board)
# - Calendar
# - Bills
# - Income
# - Transactions

