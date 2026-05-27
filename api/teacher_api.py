from flask import Blueprint, request, jsonify, g
from werkzeug.security import generate_password_hash
from auth import login_required, admin_required
from db import query, execute
import random
import string

teacher_bp = Blueprint('teacher', __name__)
MAX_CLASSES_PER_TEACHER = 5


def _generate_password():
    return 'Tc' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@teacher_bp.route('/api/teachers', methods=['GET'])
@admin_required
def get_teachers():
    search = request.args.get('search', '').strip()
    users = query("SELECT id, username FROM users WHERE role = 'teacher' ORDER BY id DESC")
    result = []
    for u in users:
        classes = query(
            """SELECT tc.*, cl.name AS college_name, m.name AS major_name
               FROM teacher_classes tc
               JOIN school.colleges cl ON tc.college_code = cl.code
               JOIN school.majors m ON tc.college_code = m.college_code AND tc.major_code = m.code
               WHERE tc.user_id = ?""",
            (u['id'],)
        )
        if search and search not in u['username']:
            if not any(search in (c['college_name'] + c['major_name']) for c in classes):
                continue
        result.append({
            'user_id': u['id'],
            'username': u['username'],
            'classes': [{
                'college_code': c['college_code'],
                'college_name': c['college_name'],
                'major_code': c['major_code'],
                'major_name': c['major_name'],
                'class_name': c['class_name']
            } for c in classes]
        })
    return jsonify(result)


@teacher_bp.route('/api/teachers', methods=['POST'])
@admin_required
def add_teacher():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    classes = data.get('classes', [])

    if not username:
        return jsonify({'error': '用户名不能为空'}), 400

    existing = query("SELECT id FROM users WHERE username = ?", (username,))
    if existing:
        return jsonify({'error': '用户名已存在'}), 400

    if len(classes) > MAX_CLASSES_PER_TEACHER:
        return jsonify({'error': f'每个教师最多分配{MAX_CLASSES_PER_TEACHER}个班级'}), 400

    if not password:
        password = _generate_password()

    user_id = execute(
        "INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
        (username, generate_password_hash(password), 'teacher')
    )

    for cls in classes:
        execute(
            "INSERT INTO teacher_classes (user_id, college_code, major_code, class_name) VALUES (?,?,?,?)",
            (user_id, cls['college_code'], cls['major_code'], cls['class_name'])
        )

    return jsonify({
        'user_id': user_id,
        'username': username,
        'password': password,
        'message': f'添加成功。教师登录账号: {username}，密码: {password}'
    }), 201


@teacher_bp.route('/api/teachers/<int:user_id>', methods=['PUT'])
@admin_required
def update_teacher(user_id):
    user = query("SELECT * FROM users WHERE id = ? AND role = 'teacher'", (user_id,), one=True)
    if not user:
        return jsonify({'error': '教师不存在'}), 404

    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    classes = data.get('classes', [])

    if not username:
        return jsonify({'error': '用户名不能为空'}), 400

    existing = query("SELECT id FROM users WHERE username = ? AND id != ?", (username, user_id))
    if existing:
        return jsonify({'error': '用户名已存在'}), 400

    if len(classes) > MAX_CLASSES_PER_TEACHER:
        return jsonify({'error': f'每个教师最多分配{MAX_CLASSES_PER_TEACHER}个班级'}), 400

    if username != user['username']:
        execute("UPDATE users SET username = ? WHERE id = ?", (username, user_id))

    if password:
        execute("UPDATE users SET password_hash = ? WHERE id = ?",
                (generate_password_hash(password), user_id))

    execute("DELETE FROM teacher_classes WHERE user_id = ?", (user_id,))
    for cls in classes:
        execute(
            "INSERT INTO teacher_classes (user_id, college_code, major_code, class_name) VALUES (?,?,?,?)",
            (user_id, cls['college_code'], cls['major_code'], cls['class_name'])
        )

    return jsonify({'message': '更新成功'})


@teacher_bp.route('/api/teachers/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_teacher(user_id):
    user = query("SELECT * FROM users WHERE id = ? AND role = 'teacher'", (user_id,), one=True)
    if not user:
        return jsonify({'error': '教师不存在'}), 404

    execute("DELETE FROM teacher_classes WHERE user_id = ?", (user_id,))
    execute("DELETE FROM users WHERE id = ?", (user_id,))
    return jsonify({'message': '删除成功'})


@teacher_bp.route('/api/teachers/me/classes', methods=['GET'])
@login_required
def get_my_classes():
    if g.user['role'] != 'teacher':
        return jsonify([])
    classes = query(
        """SELECT tc.*, cl.name AS college_name, m.name AS major_name
           FROM teacher_classes tc
           JOIN school.colleges cl ON tc.college_code = cl.code
           JOIN school.majors m ON tc.college_code = m.college_code AND tc.major_code = m.code
           WHERE tc.user_id = ?""",
        (g.user['user_id'],)
    )
    return jsonify([{
        'college_code': c['college_code'],
        'college_name': c['college_name'],
        'major_code': c['major_code'],
        'major_name': c['major_name'],
        'class_name': c['class_name']
    } for c in classes])
