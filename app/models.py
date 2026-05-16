from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Date, CheckConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    parent_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parent = relationship("Department", remote_side=[id], backref="children")
    employees = relationship("Employee", back_populates="department", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("char_length(name) >= 1", name="name_not_empty"),
    )


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    department_id = Column(Integer, ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    full_name = Column(String(200), nullable=False)
    position = Column(String(200), nullable=False)
    hired_at = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    department = relationship("Department", back_populates="employees")

    __table_args__ = (
        CheckConstraint("char_length(full_name) >= 1", name="full_name_not_empty"),
        CheckConstraint("char_length(position) >= 1", name="position_not_empty"),
    )