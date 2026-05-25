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


@student_bp.route('/api/students/next-no', methods=['GET'])
@teacher_or_admin
def get_next_student_no():
    year = request.args.get('year', '2024')
    college = request.args.get('college', '01')
    major = request.args.get('major', '01')
    cls = request.args.get('class', '01')
    prefix = year[2:] + college + major + cls
    existing = query(
        "SELECT student_no FROM students WHERE student_no LIKE ? ORDER BY student_no DESC LIMIT 1",
        (f'{prefix}%',)
    )
    if existing:
        last_seq = int(existing[0]['student_no'][-2:])
        seq = str(last_seq + 1).zfill(2)
    else:
        seq = '01'
    return jsonify({'student_no': prefix + seq, 'class_name': f'{prefix[:6]}班'})


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
