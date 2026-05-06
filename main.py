from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import prestamos

app = FastAPI(
    title="Portal Mi Banco - Modulo Prestamos",
    version="1.0.0",
    description="API del simulador de prestamos con documentacion automatica"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(prestamos.router, prefix="/api/prestamos", tags=["Prestamos"])
