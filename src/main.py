from fastapi import FastAPI
from .app.router import router

app = FastAPI(
    title="Environmental Log Reports API",
    description="API para insertar logs y obtener reportes",
    version="1.0"
)

app.include_router(router)