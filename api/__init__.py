from api.auth_api import auth_bp
from api.student_api import student_bp
from api.grade_api import grade_bp
from api.course_api import course_bp
from api.teacher_api import teacher_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(grade_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(teacher_bp)
