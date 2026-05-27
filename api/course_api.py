from flask import Blueprint, request, jsonify, g
from auth import login_required
from db import query

course_bp = Blueprint('course', __name__)


@course_bp.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    college_code = request.args.get('college_code', '').strip()
    major_code = request.args.get('major_code', '').strip()

    if g.user['role'] == 'teacher':
        sql = """
            SELECT DISTINCT c.*, cl.name AS college_name
            FROM teacher_classes tc
            JOIN courses c ON tc.college_code = c.college_code AND tc.major_code = c.major_code
            JOIN colleges cl ON c.college_code = cl.code
            WHERE tc.user_id = ?
        """
        args = [g.user['user_id']]
        if college_code:
            sql += " AND c.college_code = ?"
            args.append(college_code)
        if major_code:
            sql += " AND c.major_code = ?"
            args.append(major_code)
        sql += " ORDER BY c.college_code, c.code"
        return jsonify(query(sql, args))

    where = []
    args = []
    if college_code:
        where.append("c.college_code = ?")
        args.append(college_code)
    if major_code:
        where.append("c.major_code = ?")
        args.append(major_code)
    sql = """
        SELECT c.*, cl.name AS college_name
        FROM courses c
        JOIN colleges cl ON c.college_code = cl.code
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY c.college_code, c.code"
    return jsonify(query(sql, args))


@course_bp.route('/api/colleges', methods=['GET'])
@login_required
def get_colleges():
    if g.user['role'] == 'teacher':
        rows = query(
            """SELECT DISTINCT cl.code, cl.name
               FROM teacher_classes tc
               JOIN colleges cl ON tc.college_code = cl.code
               WHERE tc.user_id = ?
               ORDER BY cl.code""",
            (g.user['user_id'],)
        )
        return jsonify(rows)

    rows = query("SELECT code, name FROM colleges ORDER BY code")
    return jsonify(rows)


@course_bp.route('/api/majors', methods=['GET'])
@login_required
def get_majors():
    college_code = request.args.get('college_code', '').strip()

    if g.user['role'] == 'teacher':
        sql = """
            SELECT DISTINCT m.id, m.code, m.name, m.college_code
            FROM teacher_classes tc
            JOIN majors m ON tc.college_code = m.college_code AND tc.major_code = m.code
            WHERE tc.user_id = ?
        """
        args = [g.user['user_id']]
        if college_code:
            sql += " AND m.college_code = ?"
            args.append(college_code)
        sql += " ORDER BY m.college_code, m.code"
        return jsonify(query(sql, args))

    if college_code:
        rows = query(
            "SELECT id, code, name, college_code FROM majors WHERE college_code = ? ORDER BY code",
            (college_code,)
        )
    else:
        rows = query("SELECT id, code, name, college_code FROM majors ORDER BY college_code, code")
    return jsonify(rows)
