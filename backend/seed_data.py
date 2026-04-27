"""
Seed Data Script
Creates sample data for testing
"""

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app import models, schemas, crud, auth


def create_sample_data():
    """Create sample students, teachers, and admin users"""
    db = SessionLocal()
    
    try:
        # Create admin user
        admin_user = crud.create_user(db, schemas.UserCreate(
            username="admin",
            password="admin123",
            role="admin",
            full_name="Administrator"
        ))
        print(f"Created admin user: {admin_user.username}")
        
        # Create teacher user
        teacher_user = crud.create_user(db, schemas.UserCreate(
            username="teacher1",
            password="teacher123",
            role="teacher",
            full_name="John Smith"
        ))
        print(f"Created teacher user: {teacher_user.username}")
        
        # Create sample students
        students_data = [
            {
                "user": {"username": "student1", "password": "student123", "role": "student", "full_name": "Alice Johnson"},
                "student": {"student_id": "STU001", "full_name": "Alice Johnson", "class_name": "Grade 10-A", "parent_contact": "+1234567890"}
            },
            {
                "user": {"username": "student2", "password": "student123", "role": "student", "full_name": "Bob Williams"},
                "student": {"student_id": "STU002", "full_name": "Bob Williams", "class_name": "Grade 10-A", "parent_contact": "+1234567891"}
            },
            {
                "user": {"username": "student3", "password": "student123", "role": "student", "full_name": "Carol Davis"},
                "student": {"student_id": "STU003", "full_name": "Carol Davis", "class_name": "Grade 10-B", "parent_contact": "+1234567892"}
            },
            {
                "user": {"username": "student4", "password": "student123", "role": "student", "full_name": "David Brown"},
                "student": {"student_id": "STU004", "full_name": "David Brown", "class_name": "Grade 10-B", "parent_contact": "+1234567893"}
            },
            {
                "user": {"username": "student5", "password": "student123", "role": "student", "full_name": "Emma Wilson"},
                "student": {"student_id": "STU005", "full_name": "Emma Wilson", "class_name": "Grade 11-A", "parent_contact": "+1234567894"}
            }
        ]
        
        for data in students_data:
            # Create user
            user = crud.create_user(db, schemas.UserCreate(**data["user"]))
            
            # Create student
            student_data = data["student"]
            student = crud.create_student(db, schemas.StudentCreate(
                user_id=user.id,
                student_id=student_data["student_id"],
                full_name=student_data["full_name"],
                class_name=student_data["class_name"],
                parent_contact=student_data["parent_contact"]
            ))
            print(f"Created student: {student.full_name} ({student.student_id})")
        
        print("\nSample data created successfully!")
        print("\nLogin credentials:")
        print("  Admin:    admin / admin123")
        print("  Teacher:  teacher1 / teacher123")
        print("  Students: student1-5 / student123")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Create tables first
    Base.metadata.create_all(bind=engine)
    
    # Then create sample data
    create_sample_data()
