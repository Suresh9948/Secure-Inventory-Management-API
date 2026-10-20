from fastapi import FastAPI
from app.core.config import settings
from app.routers import auth, users, inventory, reports

app = FastAPI(title=settings.app_name, version="1.0.0")
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(users.router, prefix=settings.api_v1_prefix)
app.include_router(inventory.router, prefix=settings.api_v1_prefix)
app.include_router(reports.router, prefix=settings.api_v1_prefix)

@app.get("/")
def root():
    return {"message": "Secure Inventory Management API is running", "docs": "/docs"}
