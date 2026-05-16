from typing import Optional
from sqlalchemy.orm import Session
from app.models import Department


def check_circular_reference(db: Session, department_id: int, new_parent_id: int) -> bool:
    if department_id == new_parent_id:
        return True

    current = db.query(Department).filter(Department.id == new_parent_id).first()
    while current:
        if current.parent_id == department_id:
            return True
        current = current.parent
    return False


def check_unique_name_in_parent(db: Session, name: str, parent_id: Optional[int],
                                exclude_id: Optional[int] = None) -> bool:
    query = db.query(Department).filter(
        Department.name == name,
        Department.parent_id == parent_id
    )
    if exclude_id:
        query = query.filter(Department.id != exclude_id)
    return query.first() is None