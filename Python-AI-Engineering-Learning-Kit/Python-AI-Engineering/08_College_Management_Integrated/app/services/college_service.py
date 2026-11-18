from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.college import Student


def student_details(db: Session, student_id: int) -> dict:
    row = db.get(Student, student_id)
    if not row:
        return {"error": "Student not found"}
    return {"student_id": row.id, "name": row.name, "department": row.department, "semester": row.semester}


def attendance_details(db: Session, student_id: int) -> dict:
    row = db.get(Student, student_id)
    if not row or not row.attendance:
        return {"error": "Attendance not found"}
    a = row.attendance
    percentage = round(a.attended_classes / a.total_classes * 100, 2) if a.total_classes else 0
    return {"student_id": student_id, "attended_classes": a.attended_classes,
            "total_classes": a.total_classes, "percentage": percentage}


def fee_details(db: Session, student_id: int) -> dict:
    row = db.get(Student, student_id)
    if not row or not row.fee:
        return {"error": "Fee record not found"}
    f = row.fee
    return {"student_id": student_id, "total_amount": f.total_amount,
            "paid_amount": f.paid_amount, "pending_amount": f.total_amount - f.paid_amount}
