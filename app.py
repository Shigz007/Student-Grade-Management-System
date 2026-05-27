from flask import Flask, render_template, send_from_directory
from flask_cors import CORS
from config import SECRET_KEY
from db import init_db
from api import register_blueprints

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app, supports_credentials=True)

register_blueprints(app)


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('boomerang-free-bootstrap-ui-kit-master/assets', filename)


# === Login ===
@app.route('/login')
def login_page():
    return render_template('login.html')


# === Admin ===
@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')


@app.route('/admin/students')
def admin_students():
    return render_template('admin/students.html')


@app.route('/admin/grades')
def admin_grades():
    return render_template('admin/grades.html')


@app.route('/admin/teachers')
def admin_teachers():
    return render_template('admin/teachers.html')


@app.route('/admin/schedules')
def admin_schedules():
    return render_template('admin/schedules.html')


@app.route('/admin/courses')
def admin_courses():
    return render_template('admin/courses.html')


@app.route('/teacher/schedules')
def teacher_schedules():
    return render_template('teacher/schedules.html')


# === Teacher ===
@app.route('/teacher')
def teacher_dashboard():
    return render_template('teacher/dashboard.html')


@app.route('/teacher/students')
def teacher_students():
    return render_template('teacher/students.html')


@app.route('/teacher/grades')
def teacher_grades():
    return render_template('teacher/grades.html')


# === Student ===
@app.route('/student')
def student_dashboard():
    return render_template('student/dashboard.html')


@app.route('/student/grades')
def student_grades():
    return render_template('student/grades.html')


# === Root redirect ===
@app.route('/')
def index():
    return render_template('login.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
