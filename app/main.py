from fastapi import FastAPI
from app.routers import departments, employees
from app.database import engine, Base
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Организационная структура API",
    description="API для управления подразделениями и сотрудниками",
    version="1.0.0"
)

app.include_router(departments.router)
app.include_router(employees.router)

@app.get("/")
def root():
    return {"message": "Организационная структура API", "docs": "/docs"}