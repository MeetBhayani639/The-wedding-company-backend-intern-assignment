from fastapi import FastAPI
from app.routers import org, auth

app = FastAPI(
    title="The Wedding Company - Organization Management Service",
    description="Multi-tenant backend with dynamic MongoDB collections per organization",
    version="1.0.0"
)

app.include_router(org.router)
app.include_router(auth.router)

@app.get("/")
def home():
    return {"message": "Welcome to The Wedding Company Backend API"}