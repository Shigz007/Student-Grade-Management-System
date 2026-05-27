from flask import Blueprint, request, jsonify, g
from auth import login_required, admin_required
from db import query, execute

course_bp = Blueprint('course', __name__)


@course_bp.route('/api/courses', methods=['GET'])
@login_required
def get_courses():
    college_code = request.args.get('college_code', '').strip()
    major_code = request.args.get('major_code', '').strip()

    if g.user['role'] == 'teacher':
        sql = """
            SELECT DISTINCT c.*, cl.name AS college_name, m.name AS major_name
            FROM teacher_classes tc
            JOIN courses c ON tc.college_code = c.college_code AND tc.major_code = c.major_code
            JOIN colleges cl ON c.college_code = cl.code
            LEFT JOIN majors m ON c.college_code = m.college_code AND c.major_code = m.code
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
        SELECT c.*, cl.name AS college_name, m.name AS major_name
        FROM courses c
        JOIN colleges cl ON c.college_code = cl.code
        LEFT JOIN majors m ON c.college_code = m.college_code AND c.major_code = m.code
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY c.college_code, c.code"
    return jsonify(query(sql, args))


@course_bp.route('/api/courses', methods=['POST'])
@admin_required
def add_course():
    data = request.get_json()
    code = data.get('code', '').strip()
    name = data.get('name', '').strip()
    college_code = data.get('college_code', '').strip()
    major_code = data.get('major_code', '').strip()

    if not name or not college_code or not major_code:
        return jsonify({'error': '课程名称、学院和专业不能为空'}), 400

    if not code:
        rows = query(
            "SELECT code FROM courses WHERE college_code = ? AND major_code = ? ORDER BY CAST(code AS INTEGER) DESC LIMIT 1",
            (college_code, major_code)
        )
        max_num = int(rows[0]['code']) if rows else 0
        code = str(max_num + 1).zfill(2)

    existing = query("SELECT id FROM courses WHERE college_code = ? AND major_code = ? AND code = ?",
                     (college_code, major_code, code))
    if existing:
        return jsonify({'error': '课程代码冲突'}), 400

    cid = execute(
        "INSERT INTO courses (code, name, college_code, major_code) VALUES (?,?,?,?)",
        (code, name, college_code, major_code)
    )
    return jsonify({'id': cid, 'message': '添加成功'}), 201


@course_bp.route('/api/courses/<int:cid>', methods=['PUT'])
@admin_required
def update_course(cid):
    course = query("SELECT * FROM courses WHERE id = ?", (cid,), one=True)
    if not course:
        return jsonify({'error': '课程不存在'}), 404

    data = request.get_json()
    code = data.get('code', '').strip()
    name = data.get('name', '').strip()
    college_code = data.get('college_code', '').strip()
    major_code = data.get('major_code', '').strip()

    if not name or not college_code or not major_code:
        return jsonify({'error': '课程名称、学院和专业不能为空'}), 400

    if not code:
        code = course['code']

    existing = query("SELECT id FROM courses WHERE college_code = ? AND major_code = ? AND code = ? AND id != ?",
                     (college_code, major_code, code, cid))
    if existing:
        return jsonify({'error': '课程代码冲突'}), 400

    old_college = course['college_code']
    old_major = course['major_code'] or ''
    execute(
        "UPDATE courses SET code=?, name=?, college_code=?, major_code=? WHERE id=?",
        (code, name, college_code, major_code, cid)
    )
    if college_code != old_college or major_code != old_major:
        renumber_courses(old_college, old_major)
    renumber_courses(college_code, major_code)
    return jsonify({'message': '更新成功'})


@course_bp.route('/api/courses/<int:cid>', methods=['DELETE'])
@admin_required
def delete_course(cid):
    course = query("SELECT * FROM courses WHERE id = ?", (cid,), one=True)
    if not course:
        return jsonify({'error': '课程不存在'}), 404
    college_code = course['college_code']
    major_code = course['major_code']
    execute("DELETE FROM courses WHERE id = ?", (cid,))
    renumber_courses(college_code, major_code)
    return jsonify({'message': '删除成功'})


# --- Colleges ---

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


@course_bp.route('/api/colleges', methods=['POST'])
@admin_required
def add_college():
    data = request.get_json()
    code = data.get('code', '').strip()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': '学院名称不能为空'}), 400
    if not code:
        rows = query("SELECT code FROM colleges ORDER BY CAST(code AS INTEGER) DESC LIMIT 1")
        max_num = int(rows[0]['code']) if rows else 0
        code = str(max_num + 1).zfill(2)
    existing = query("SELECT code FROM colleges WHERE code = ?", (code,))
    if existing:
        return jsonify({'error': '学院代码已存在'}), 400
    execute("INSERT INTO colleges (code, name) VALUES (?,?)", (code, name))
    return jsonify({'message': '添加成功'}), 201


@course_bp.route('/api/colleges/<code>', methods=['PUT'])
@admin_required
def update_college(code):
    college = query("SELECT * FROM colleges WHERE code = ?", (code,), one=True)
    if not college:
        return jsonify({'error': '学院不存在'}), 404
    data = request.get_json()
    name = data.get('name', '').strip()
    if not name:
        return jsonify({'error': '学院名称不能为空'}), 400
    execute("UPDATE colleges SET name=? WHERE code=?", (name, code))
    return jsonify({'message': '更新成功'})


@course_bp.route('/api/colleges/<code>', methods=['DELETE'])
@admin_required
def delete_college(code):
    college = query("SELECT * FROM colleges WHERE code = ?", (code,), one=True)
    if not college:
        return jsonify({'error': '学院不存在'}), 404
    execute("DELETE FROM colleges WHERE code = ?", (code,))
    renumber_colleges()
    return jsonify({'message': '删除成功'})


# --- Majors ---

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


@course_bp.route('/api/majors', methods=['POST'])
@admin_required
def add_major():
    data = request.get_json()
    code = data.get('code', '').strip()
    name = data.get('name', '').strip()
    college_code = data.get('college_code', '').strip()
    if not name or not college_code:
        return jsonify({'error': '专业名称和学院不能为空'}), 400
    if not code:
        rows = query(
            "SELECT code FROM majors WHERE college_code = ? ORDER BY CAST(code AS INTEGER) DESC LIMIT 1",
            (college_code,)
        )
        max_num = int(rows[0]['code']) if rows else 0
        code = str(max_num + 1).zfill(2)
    existing = query("SELECT id FROM majors WHERE college_code = ? AND code = ?", (college_code, code))
    if existing:
        return jsonify({'error': '该学院下专业代码已存在'}), 400
    mid = execute(
        "INSERT INTO majors (code, name, college_code) VALUES (?,?,?)",
        (code, name, college_code)
    )
    return jsonify({'id': mid, 'message': '添加成功'}), 201


@course_bp.route('/api/majors/<int:mid>', methods=['PUT'])
@admin_required
def update_major(mid):
    major = query("SELECT * FROM majors WHERE id = ?", (mid,), one=True)
    if not major:
        return jsonify({'error': '专业不存在'}), 404
    data = request.get_json()
    code = data.get('code', '').strip()
    name = data.get('name', '').strip()
    college_code = data.get('college_code', '').strip()
    if not name or not college_code:
        return jsonify({'error': '专业名称和学院不能为空'}), 400
    if not code:
        code = major['code']
    existing = query("SELECT id FROM majors WHERE college_code = ? AND code = ? AND id != ?", (college_code, code, mid))
    if existing:
        return jsonify({'error': '该学院下专业代码已存在'}), 400
    old_college = major['college_code']
    execute("UPDATE majors SET code=?, name=?, college_code=? WHERE id=?", (code, name, college_code, mid))
    renumber_majors(old_college)
    if college_code != old_college:
        renumber_majors(college_code)
    return jsonify({'message': '更新成功'})


@course_bp.route('/api/majors/<int:mid>', methods=['DELETE'])
@admin_required
def delete_major(mid):
    major = query("SELECT * FROM majors WHERE id = ?", (mid,), one=True)
    if not major:
        return jsonify({'error': '专业不存在'}), 404
    college_code = major['college_code']
    execute("DELETE FROM majors WHERE id = ?", (mid,))
    renumber_majors(college_code)
    return jsonify({'message': '删除成功'})


def renumber_courses(college_code, major_code):
    rows = query(
        "SELECT id FROM courses WHERE college_code = ? AND major_code = ? ORDER BY CAST(code AS INTEGER), id",
        (college_code, major_code)
    )
    for i, row in enumerate(rows, 1):
        execute("UPDATE courses SET code = ? WHERE id = ?", (str(i).zfill(2), row['id']))


def renumber_majors(college_code):
    rows = query(
        "SELECT id, code AS old_code FROM majors WHERE college_code = ? ORDER BY CAST(code AS INTEGER), id",
        (college_code,)
    )
    for i, row in enumerate(rows, 1):
        new_code = str(i).zfill(2)
        if row['old_code'] != new_code:
            execute("UPDATE majors SET code = ? WHERE id = ?", (new_code, row['id']))
            execute("UPDATE courses SET major_code = ? WHERE college_code = ? AND major_code = ?",
                    (new_code, college_code, row['old_code']))
            execute("UPDATE students SET major_code = ? WHERE college_code = ? AND major_code = ?",
                    (new_code, college_code, row['old_code']))
            execute("UPDATE teacher_classes SET major_code = ? WHERE college_code = ? AND major_code = ?",
                    (new_code, college_code, row['old_code']))
            execute("UPDATE schedules SET major_code = ? WHERE college_code = ? AND major_code = ?",
                    (new_code, college_code, row['old_code']))


def renumber_colleges():
    rows = query("SELECT code AS old_code FROM colleges ORDER BY CAST(code AS INTEGER)")
    for i, row in enumerate(rows, 1):
        new_code = str(i).zfill(2)
        if row['old_code'] != new_code:
            execute("UPDATE colleges SET code = ? WHERE code = ?", (new_code, row['old_code']))
            execute("UPDATE majors SET college_code = ? WHERE college_code = ?", (new_code, row['old_code']))
            execute("UPDATE courses SET college_code = ? WHERE college_code = ?", (new_code, row['old_code']))
            execute("UPDATE students SET college_code = ? WHERE college_code = ?", (new_code, row['old_code']))
            execute("UPDATE teacher_classes SET college_code = ? WHERE college_code = ?", (new_code, row['old_code']))
            execute("UPDATE schedules SET college_code = ? WHERE college_code = ?", (new_code, row['old_code']))
