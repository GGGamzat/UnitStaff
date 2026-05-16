from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
from app import crud, schemas
from app.database import get_db

router = APIRouter(prefix="/departments", tags=["departments"])

@router.post("/", response_model=schemas.DepartmentResponse, status_code=status.HTTP_201_CREATED)
def create_department(department: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    return crud.create_department(db, department)

@router.get("/{department_id}", response_model=schemas.DepartmentResponse)
def get_department(
    department_id: int,
    depth: int = Query(1, ge=1, le=5),
    include_employees: bool = Query(True),
    db: Session = Depends(get_db)
):
    return crud.get_department_tree(db, department_id, depth, include_employees)

@router.patch("/{department_id}", response_model=schemas.DepartmentResponse)
def update_department(
    department_id: int,
    department_update: schemas.DepartmentUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_department(db, department_id, department_update)

@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_department(
    department_id: int,
    mode: str = Query(..., regex="^(cascade|reassign)$"),
    reassign_to_department_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    crud.delete_department(db, department_id, mode, reassign_to_department_id)
    return None