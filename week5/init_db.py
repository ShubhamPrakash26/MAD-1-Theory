# File: init_db.py
from app import app, db, Course

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()

        # Check if courses already exist
        if Course.query.count() == 0:
            # Add courses
            courses = [
                Course(
                    course_code='CSE01',
                    course_name='MAD I',
                    course_description='Modern Application Development - I'
                ),
                Course(
                    course_code='CSE02',
                    course_name='DBMS',
                    course_description='Database management Systems'
                ),
                Course(
                    course_code='CSE03',
                    course_name='PDSA',
                    course_description='Programming, Data Structures and Algorithms using Python'
                ),
                Course(
                    course_code='BST13',
                    course_name='BDM',
                    course_description='Business Data Management'
                )
            ]

            # Add all courses to the session
            for course in courses:
                db.session.add(course)
            
            # Commit the changes
            db.session.commit()
            print("Database initialized with course data!")
        else:
            print("Courses already exist in the database!")

if __name__ == '__main__':
    init_db()