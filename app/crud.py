from sqlalchemy.orm import Session
from sqlalchemy import asc
from app import models, schemas
from app.utils.validators import check_circular_reference, check_unique_name_in_parent
from fastapi import HTTPException


def create_department(db: Session, department: schemas.DepartmentCreate):
    if not check_unique_name_in_parent(db, department.name, department.parent_id):
        raise HTTPException(status_code=409, detail="Подразделение с таким именем уже существует на этом уровне")

    db_department = models.Department(name=department.name, parent_id=department.parent_id)
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    return db_department


def update_department(db: Session, department_id: int, department_update: schemas.DepartmentUpdate):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Подразделение не найдено")

    if department_update.name is not None:
        if not check_unique_name_in_parent(db, department_update.name, db_department.parent_id, department_id):
            raise HTTPException(status_code=409, detail="Подразделение с таким именем уже существует на этом уровне")
        db_department.name = department_update.name

    if department_update.parent_id is not None:
        if check_circular_reference(db, department_id, department_update.parent_id):
            raise HTTPException(status_code=409, detail="Нельзя создать циклическую ссылку в дереве")
        db_department.parent_id = department_update.parent_id

    db.commit()
    db.refresh(db_department)
    return db_department


def delete_department(db: Session, department_id: int, mode: str, reassign_to: int = None):
    db_department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="Подразделение не найдено")

    if mode == "reassign":
        if not reassign_to:
            raise HTTPException(status_code=400,
                                detail="При mode=reassign необходимо указать reassign_to_department_id")

        target_department = db.query(models.Department).filter(models.Department.id == reassign_to).first()
        if not target_department:
            raise HTTPException(status_code=404, detail="Целевое подразделение не найдено")

        db.query(models.Employee).filter(models.Employee.department_id == department_id).update(
            {"department_id": reassign_to}
        )

        db.query(models.Department).filter(models.Department.parent_id == department_id).update(
            {"parent_id": reassign_to}
        )

        db.delete(db_department)
        db.commit()

    elif mode == "cascade":
        db.delete(db_department)
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Неверный режим удаления. Используйте 'cascade' или 'reassign'")


def get_department_tree(db: Session, department_id: int, depth: int = 1, include_employees: bool = True):
    department = db.query(models.Department).filter(models.Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Подразделение не найдено")

    return _build_tree(db, department, depth, include_employees)


def _build_tree(db: Session, department: models.Department, depth: int, include_employees: bool):
    from app.schemas import DepartmentResponse, EmployeeResponse

    employees = []
    if include_employees:
        employees = [
            EmployeeResponse.model_validate(emp)
            for emp in db.query(models.Employee)
            .filter(models.Employee.department_id == department.id)
            .order_by(asc(models.Employee.created_at))
            .all()
        ]

    children = []
    if depth > 1:
        child_depts = db.query(models.Department).filter(models.Department.parent_id == department.id).all()
        for child in child_depts:
            children.append(_build_tree(db, child, depth - 1, include_employees))

    return DepartmentResponse(
        id=department.id,
        name=department.name,
        parent_id=department.parent_id,
        created_at=department.created_at,
        employees=employees,
        children=children
    )