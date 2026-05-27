import random
from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash
from auth import login_required, teacher_or_admin, admin_required
from db import query, execute

student_bp = Blueprint('student', __name__)
DEFAULT_STUDENT_PASSWORD = 'Ad112233'


@student_bp.route('/api/students', methods=['GET'])
@login_required
def get_students():
    search = request.args.get('search', '').strip()
    class_name = request.args.get('class_name', '').strip()

    if g.user['role'] == 'student':
        students = query("SELECT * FROM students WHERE name = ?", (g.user['username'],))
    elif g.user['role'] == 'teacher':
        tcs = query("SELECT college_code, major_code, class_name FROM teacher_classes WHERE user_id = ?",
                    (g.user['user_id'],))
        if not tcs:
            return jsonify([])
        conds = []
        targs = []
        for tc in tcs:
            conds.append("(college_code = ? AND major_code = ? AND SUBSTR(student_no, 7, 2) = ?)")
            targs.extend([tc['college_code'], tc['major_code'], tc['class_name']])
        sql = "SELECT * FROM students WHERE (" + " OR ".join(conds) + ")"
        if search:
            sql += " AND (name LIKE ? OR student_no LIKE ?)"
            targs.extend([f'%{search}%', f'%{search}%'])
        if class_name:
            sql += " AND class_name = ?"
            targs.append(class_name)
        sql += " ORDER BY id DESC"
        students = query(sql, targs)
    else:
        where = []
        args = []
        if search:
            where.append("(name LIKE ? OR student_no LIKE ?)")
            args.extend([f'%{search}%', f'%{search}%'])
        if class_name:
            where.append("class_name = ?")
            args.append(class_name)
        sql = "SELECT * FROM students"
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY id DESC"
        students = query(sql, args)

    return jsonify(students)


def _gen_student_no(class_prefix):
    existing = query(
        "SELECT student_no FROM students WHERE student_no LIKE ? ORDER BY CAST(SUBSTR(student_no, 9, 2) AS INTEGER) DESC LIMIT 1",
        (f'{class_prefix}%',)
    )
    if existing:
        last_seq = int(existing[0]['student_no'][-2:])
        seq = str(last_seq + 1).zfill(2)
    else:
        seq = '01'
    return {'student_no': class_prefix + seq, 'class_seq': class_prefix[6:8]}


@student_bp.route('/api/students/next-no', methods=['GET'])
@teacher_or_admin
def get_next_student_no():
    year = request.args.get('year', '2024')
    college = request.args.get('college', '01')
    major = request.args.get('major', '01')
    cls = request.args.get('class', '').strip()

    MAX_PER_CLASS = 50
    NEW_CLASS_THRESHOLD = random.randint(30, 40)
    prefix = year[2:] + college + major

    if cls:
        class_prefix = prefix + cls
        count = query(
            "SELECT COUNT(*) as cnt FROM students WHERE student_no LIKE ?",
            (f'{class_prefix}%',)
        )[0]['cnt']
        if count >= MAX_PER_CLASS:
            return jsonify({'error': f'该班级已满（{MAX_PER_CLASS}人）'}), 400
        return jsonify(_gen_student_no(class_prefix))

    classes = query(
        "SELECT SUBSTR(student_no, 7, 2) AS class_seq, COUNT(*) AS cnt FROM students WHERE student_no LIKE ? GROUP BY class_seq ORDER BY class_seq",
        (f'{prefix}%',)
    )

    if not classes:
        return jsonify(_gen_student_no(prefix + '01'))

    best_class = None
    min_count = MAX_PER_CLASS + 1
    for c in classes:
        cnt = c['cnt']
        if cnt < MAX_PER_CLASS and cnt < min_count:
            min_count = cnt
            best_class = c['class_seq']

    if best_class and min_count < NEW_CLASS_THRESHOLD:
        return jsonify(_gen_student_no(prefix + best_class))

    last_class = max(int(c['class_seq']) for c in classes)
    next_class = str(last_class + 1).zfill(2)
    if int(next_class) > 99:
        return jsonify({'error': '该专业所有班级已满'}), 400
    return jsonify(_gen_student_no(prefix + next_class))


@student_bp.route('/api/students/classes', methods=['GET'])
@teacher_or_admin
def get_classes():
    year = request.args.get('year', '')
    college = request.args.get('college', '')
    major = request.args.get('major', '')
    if not year or not college or not major:
        return jsonify([])
    prefix = year[2:] + college + major
    rows = query(
        "SELECT SUBSTR(student_no, 7, 2) AS class_seq, COUNT(*) AS cnt FROM students WHERE student_no LIKE ? GROUP BY class_seq ORDER BY class_seq",
        (f'{prefix}%',)
    )
    return jsonify([{'class_seq': r['class_seq'], 'count': r['cnt']} for r in rows])


@student_bp.route('/api/students', methods=['POST'])
@teacher_or_admin
def add_student():
    data = request.get_json()
    student_no = data.get('student_no', '').strip()
    name = data.get('name', '').strip()

    if not student_no or not name:
        return jsonify({'error': '学号和姓名不能为空'}), 400

    existing = query("SELECT id FROM students WHERE student_no = ?", (student_no,))
    if existing:
        return jsonify({'error': '学号已存在'}), 400

    existing_user = query("SELECT id FROM users WHERE username = ?", (name,))
    if existing_user:
        return jsonify({'error': '已存在同名账号，请使用不同的姓名'}), 400

    sid = execute(
        """INSERT INTO students (student_no, name, gender, enrollment_year, college_code, major_code, class_name, phone, email)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (student_no, name, data.get('gender', ''),
         data.get('enrollment_year', ''), data.get('college_code', ''),
         data.get('major_code', ''), data.get('class_name', ''),
         data.get('phone', ''), data.get('email', ''))
    )
    execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
        (name, generate_password_hash(DEFAULT_STUDENT_PASSWORD), 'student')
    )
    return jsonify({
        'id': sid,
        'message': f'添加成功。学生登录账号: {name}，密码: {DEFAULT_STUDENT_PASSWORD}',
        'account': {'username': name, 'password': DEFAULT_STUDENT_PASSWORD}
    }), 201


@student_bp.route('/api/students/<int:sid>', methods=['PUT'])
@teacher_or_admin
def update_student(sid):
    data = request.get_json()
    student = query("SELECT * FROM students WHERE id = ?", (sid,), one=True)
    if not student:
        return jsonify({'error': '学生不存在'}), 404

    execute(
        """UPDATE students SET student_no=?, name=?, gender=?, enrollment_year=?,
           college_code=?, major_code=?, class_name=?, phone=?, email=? WHERE id=?""",
        (data.get('student_no', student['student_no']),
         data.get('name', student['name']),
         data.get('gender', student['gender']),
         data.get('enrollment_year', student.get('enrollment_year', '')),
         data.get('college_code', student.get('college_code', '')),
         data.get('major_code', student.get('major_code', '')),
         data.get('class_name', student.get('class_name', '')),
         data.get('phone', student.get('phone', '')),
         data.get('email', student.get('email', '')),
         sid)
    )
    return jsonify({'message': '更新成功'})


@student_bp.route('/api/students/<int:sid>', methods=['DELETE'])
@admin_required
def delete_student(sid):
    student = query("SELECT * FROM students WHERE id = ?", (sid,), one=True)
    if not student:
        return jsonify({'error': '学生不存在'}), 404
    execute("DELETE FROM grades WHERE student_id = ?", (sid,))
    execute("DELETE FROM users WHERE username = ? AND role = 'student'", (student['name'],))
    execute("DELETE FROM students WHERE id = ?", (sid,))
    return jsonify({'message': '删除成功'})
