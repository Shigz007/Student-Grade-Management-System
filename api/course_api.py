from flask import Blueprint, request, jsonify
from auth import login_required
from db import query

course_bp = Blueprint('course', __name__)


@course_bp.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    college_code = request.args.get('college_code', '').strip()
    if college_code:
        rows = query("SELECT * FROM courses WHERE college_code = ? ORDER BY code", (college_code,))
    else:
        rows = query("SELECT * FROM courses ORDER BY college_code, code")
    return jsonify(rows)


@course_bp.route('/api/colleges', methods=['GET'])
@login_required
def get_colleges():
    rows = query("SELECT DISTINCT college_code as code, college_name as name FROM courses ORDER BY college_code")
    return jsonify(rows)
