from fastapi import FastAPI

# Minimal FastAPI app required by tests and TestClient
app = FastAPI()

# include reports router
from crm_svc.routers.reports import reports_router

app.include_router(reports_router, prefix="/api")
