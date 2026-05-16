from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/departments", tags=["employees"])


@router.post("/{department_id}/employees", response_model=schemas.EmployeeResponse, status_code=status.HTTP_201_CREATED)
def create_employee(
        department_id: int,
        employee: schemas.EmployeeCreate,
        db: Session = Depends(get_db)
):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Подразделение не найдено")

    db_employee = models.Employee(
        department_id=department_id,
        full_name=employee.full_name.strip(),
        position=employee.position.strip(),
        hired_at=employee.hired_at
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee