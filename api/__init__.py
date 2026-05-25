from api.auth_api import auth_bp
from api.student_api import student_bp
from api.grade_api import grade_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(grade_bp)
