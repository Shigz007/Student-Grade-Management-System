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


@app.route('/')
def index():
    return render_template('dashboard.html')


@app.route('/login')
def login_page():
    return render_template('login.html')


@app.route('/students')
def students_page():
    return render_template('students.html')


@app.route('/grades')
def grades_page():
    return render_template('grades.html')


if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
