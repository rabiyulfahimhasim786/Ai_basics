from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base


class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    department: Mapped[str] = mapped_column(String(120), nullable=False)
    semester: Mapped[int] = mapped_column(Integer, nullable=False)
    attendance: Mapped["Attendance"] = relationship(back_populates="student", uselist=False)
    fee: Mapped["Fee"] = relationship(back_populates="student", uselist=False)


class Attendance(Base):
    __tablename__ = "attendance"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True)
    total_classes: Mapped[int] = mapped_column(Integer, nullable=False)
    attended_classes: Mapped[int] = mapped_column(Integer, nullable=False)
    student: Mapped[Student] = relationship(back_populates="attendance")


class Fee(Base):
    __tablename__ = "fees"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True)
    total_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    paid_amount: Mapped[int] = mapped_column(Integer, nullable=False)
    student: Mapped[Student] = relationship(back_populates="fee")
