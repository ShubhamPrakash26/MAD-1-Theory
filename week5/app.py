# File: app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
db = SQLAlchemy(app)

# Models
class Student(db.Model):
    __tablename__ = 'student'
    student_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roll_number = db.Column(db.String, unique=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String)
    enrollments = db.relationship('Enrollments', backref='student', lazy=True, cascade="all, delete-orphan")

class Course(db.Model):
    __tablename__ = 'course'
    course_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_code = db.Column(db.String, unique=True, nullable=False)
    course_name = db.Column(db.String, nullable=False)
    course_description = db.Column(db.String)

class Enrollments(db.Model):
    __tablename__ = 'enrollments'
    enrollment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    estudent_id = db.Column(db.Integer, db.ForeignKey('student.student_id'), nullable=False)
    ecourse_id = db.Column(db.Integer, db.ForeignKey('course.course_id'), nullable=False)
    course = db.relationship('Course', backref='enrollments')

# Routes
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/student/create', methods=['GET', 'POST'])
def create_student():
    if request.method == 'POST':
        roll = request.form['roll']
        
        # Check if student already exists
        existing_student = Student.query.filter_by(roll_number=roll).first()
        if existing_student:
            return render_template('exists.html')
        
        # Create new student
        student = Student(
            roll_number=roll,
            first_name=request.form['f_name'],
            last_name=request.form['l_name']
        )
        db.session.add(student)
        db.session.flush()
        
        # Create enrollments
        courses = request.form.getlist('courses')
        for course_id in courses:
            enrollment = Enrollments(
                estudent_id=student.student_id,
                ecourse_id=int(course_id)
            )
            db.session.add(enrollment)
        
        db.session.commit()
        return redirect(url_for('index'))
    
    courses = Course.query.all()
    return render_template('create.html', courses=courses)

@app.route('/student/<int:student_id>')
def student_details(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('student_details.html', student=student)

@app.route('/student/<int:student_id>/update', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        student.first_name = request.form['f_name']
        student.last_name = request.form['l_name']
        
        # Update enrollments
        Enrollments.query.filter_by(estudent_id=student_id).delete()
        
        courses = request.form.getlist('courses')
        for course_id in courses:
            enrollment = Enrollments(
                estudent_id=student_id,
                ecourse_id=int(course_id)
            )
            db.session.add(enrollment)
        
        db.session.commit()
        return redirect(url_for('index'))
    
    courses = Course.query.all()
    enrolled_courses = [e.ecourse_id for e in student.enrollments]
    return render_template('update.html', student=student, courses=courses, enrolled_courses=enrolled_courses)

@app.route('/student/<int:student_id>/delete')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

# if __name__ == '__main__':
#     app.run(debug=True)