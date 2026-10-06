from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import sys

from .core.config import settings
if settings.BASE_DIR not in sys.path:
    sys.path.insert(0, settings.BASE_DIR)
from .core.database import engine, Base, apply_db_migrations
from .core.mongo_db import mongo_manager
from .services.migrate_to_mongodb import run_migration
from .api import auth, patients, health_data, datasets, pipelines, predictions, models_admin, explanations, recommendation_routes, risk_monitoring, chat, admin_api, notifications, reports

# Initialize SQL tables & safe migrations
Base.metadata.create_all(bind=engine)
apply_db_migrations(engine)

# Trigger automatic MongoDB migration from SQLite
try:
    run_migration()
except Exception as err:
    print(f"[Main Startup Note] Migration execution: {err}")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SmartCare AI Healthcare Platform - MongoDB Database Integration",
    version="6.2.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static directory for PDF reports & assets
static_dir = os.path.join(settings.BASE_DIR, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Include API Routers
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(patients.router, prefix=settings.API_V1_STR)
app.include_router(health_data.router, prefix=settings.API_V1_STR)
app.include_router(datasets.router, prefix=settings.API_V1_STR)
app.include_router(pipelines.router, prefix=settings.API_V1_STR)
app.include_router(predictions.router, prefix=settings.API_V1_STR)
app.include_router(models_admin.router, prefix=settings.API_V1_STR)
app.include_router(explanations.router, prefix=settings.API_V1_STR)
app.include_router(recommendation_routes.router, prefix=settings.API_V1_STR)
app.include_router(risk_monitoring.router, prefix=settings.API_V1_STR)
app.include_router(chat.router, prefix=settings.API_V1_STR)
app.include_router(admin_api.router, prefix=settings.API_V1_STR)
app.include_router(notifications.router, prefix=settings.API_V1_STR)
app.include_router(reports.router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {
        "status": "ONLINE",
        "system": settings.PROJECT_NAME,
        "database": "MongoDB (smartcare_ai)",
        "modules": [
            "Module 1: Data Acquisition & Preprocessing",
            "Module 2: Comorbidity-Aware Multi-Task Risk Prediction",
            "Module 3: Explainable AI & Risk Factor Analysis",
            "Module 4: Personalized Wellness Recommendation",
            "Module 5: Risk Monitoring & Clinical Decision Support",
            "Module 6: SmartCare AI Dashboard & Wellness Chatbot",
            "MongoDB Integration: 14 Primary Collections & RBAC Audit Logging"
        ],
        "docs_url": "/docs"
    }
