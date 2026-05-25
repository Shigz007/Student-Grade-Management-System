from flask import Blueprint, request, jsonify, g
from auth import login_required, teacher_or_admin, admin_required
from db import query, execute

student_bp = Blueprint('student', __name__)


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

    sid = execute(
        "INSERT INTO students (student_no, name, gender, class_name, phone, email) VALUES (?,?,?,?,?,?)",
        (student_no, name, data.get('gender', ''), data.get('class_name', ''),
         data.get('phone', ''), data.get('email', ''))
    )
    return jsonify({'id': sid, 'message': '添加成功'}), 201


@student_bp.route('/api/students/<int:sid>', methods=['PUT'])
@teacher_or_admin
def update_student(sid):
    data = request.get_json()
    student = query("SELECT * FROM students WHERE id = ?", (sid,), one=True)
    if not student:
        return jsonify({'error': '学生不存在'}), 404

    execute(
        "UPDATE students SET student_no=?, name=?, gender=?, class_name=?, phone=?, email=? WHERE id=?",
        (data.get('student_no', student['student_no']),
         data.get('name', student['name']),
         data.get('gender', student['gender']),
         data.get('class_name', student['class_name']),
         data.get('phone', student['phone']),
         data.get('email', student['email']),
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
    execute("DELETE FROM students WHERE id = ?", (sid,))
    return jsonify({'message': '删除成功'})
