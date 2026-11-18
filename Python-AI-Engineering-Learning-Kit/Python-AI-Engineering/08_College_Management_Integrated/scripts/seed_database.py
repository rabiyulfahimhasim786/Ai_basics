from app.db.database import Base, engine, SessionLocal
from app.models.college import Student, Attendance, Fee


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        if db.get(Student, 101):
            print("Sample data already exists; no changes made.")
            return
        db.add_all([
            Student(id=101, name="Arun", department="Computer Science", semester=5,
                    attendance=Attendance(total_classes=100, attended_classes=85),
                    fee=Fee(total_amount=50000, paid_amount=40000)),
            Student(id=102, name="Rahul", department="Electrical Engineering", semester=3,
                    attendance=Attendance(total_classes=100, attended_classes=70),
                    fee=Fee(total_amount=45000, paid_amount=45000)),
        ])
        db.commit()
        print("Seeded fictional college records.")


if __name__ == "__main__":
    seed()
