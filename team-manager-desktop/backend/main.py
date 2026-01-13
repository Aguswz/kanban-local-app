#!/usr/bin/env python3
"""
🧠 Team Manager Desktop - Backend Principal
FastAPI backend con IA integrada para gestión multi-equipo
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import uvicorn
import os
import sys
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar routers
from api.teams import router as teams_router
from api.projects import router as projects_router
from api.boards import router as boards_router
from api.workload import router as workload_router
from api.ai import router as ai_router
from api.health import router as health_router

# Importar servicios
from services.database import DatabaseService
from services.ai_director import AIDirectorService
from services.workload_analyzer import WorkloadAnalyzer
from services.risk_detector import RiskDetector

# Configuración
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
FRONTEND_DIR = BASE_DIR.parent / "frontend" / "build"

# Servicios globales
db_service = None
ai_director = None
workload_analyzer = None
risk_detector = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gestión del ciclo de vida de la aplicación"""
    global db_service, ai_director, workload_analyzer, risk_detector
    
    # Startup
    logger.info("🚀 Iniciando Team Manager Backend...")
    
    # Crear directorio de datos
    DATA_DIR.mkdir(exist_ok=True)
    
    # Inicializar base de datos
    db_service = DatabaseService(DATA_DIR / "team_manager.db")
    await db_service.initialize()
    
    # Inicializar servicios de IA
    ai_director = AIDirectorService()
    workload_analyzer = WorkloadAnalyzer(db_service)
    risk_detector = RiskDetector(db_service)
    
    # Configurar servicios en la app
    app.state.db = db_service
    app.state.ai_director = ai_director
    app.state.workload_analyzer = workload_analyzer
    app.state.risk_detector = risk_detector
    
    logger.info("✅ Backend iniciado correctamente")
    logger.info(f"📁 Base de datos: {DATA_DIR / 'team_manager.db'}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Cerrando Team Manager Backend...")
    if db_service:
        await db_service.close()

# Crear aplicación FastAPI
app = FastAPI(
    title="Team Manager Desktop API",
    description="API para gestión de múltiples equipos y proyectos con IA",
    version="1.0.0",
    lifespan=lifespan
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(health_router, prefix="/api/health", tags=["health"])
app.include_router(teams_router, prefix="/api/teams", tags=["teams"])
app.include_router(projects_router, prefix="/api/projects", tags=["projects"])
app.include_router(boards_router, prefix="/api/boards", tags=["boards"])
app.include_router(workload_router, prefix="/api/workload", tags=["workload"])
app.include_router(ai_router, prefix="/api/ai", tags=["ai"])

# Servir frontend estático (en producción)
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")

@app.get("/api")
async def root():
    """Endpoint raíz de la API"""
    return {
        "message": "Team Manager Desktop API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/api/health",
            "teams": "/api/teams",
            "projects": "/api/projects",
            "boards": "/api/boards",
            "workload": "/api/workload",
            "ai": "/api/ai"
        }
    }

# Funciones de utilidad para acceder a servicios
def get_db_service() -> DatabaseService:
    """Obtener servicio de base de datos"""
    return app.state.db

def get_ai_director() -> AIDirectorService:
    """Obtener director de IA"""
    return app.state.ai_director

def get_workload_analyzer() -> WorkloadAnalyzer:
    """Obtener analizador de carga"""
    return app.state.workload_analyzer

def get_risk_detector() -> RiskDetector:
    """Obtener detector de riesgos"""
    return app.state.risk_detector

if __name__ == "__main__":
    # Configuración para desarrollo
    port = int(os.getenv("PORT", 8001))
    
    # Detectar si estamos en modo desarrollo
    is_dev = "--dev" in sys.argv or os.getenv("NODE_ENV") == "development"
    
    if is_dev:
        logger.info("🔧 Modo desarrollo activado")
        uvicorn.run(
            "main:app",
            host="127.0.0.1",
            port=port,
            reload=True,
            log_level="info"
        )
    else:
        logger.info("🚀 Modo producción")
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=port,
            log_level="warning"
        )