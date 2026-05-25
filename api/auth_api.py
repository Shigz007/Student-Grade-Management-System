from flask import Blueprint, request, jsonify, g
from werkzeug.security import check_password_hash, generate_password_hash
from auth import create_token, login_required
from db import query, execute

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '')

    user = query("SELECT * FROM users WHERE username = ?", (username,), one=True)
    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': '用户名或密码错误'}), 401

    token = create_token(user['id'], user['username'], user['role'])
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'role': user['role']
        }
    })


@auth_bp.route('/api/me', methods=['GET'])
@login_required
def me():
    return jsonify(g.user)


@auth_bp.route('/api/me', methods=['PUT'])
@login_required
def update_profile():
    data = request.get_json()
    new_name = data.get('username', '').strip()

    if not new_name:
        return jsonify({'error': '用户名不能为空'}), 400

    existing = query("SELECT id FROM users WHERE username = ? AND id != ?",
                     (new_name, g.user['user_id']))
    if existing:
        return jsonify({'error': '该用户名已被使用'}), 400

    old_username = g.user['username']

    execute("UPDATE users SET username = ? WHERE id = ?",
            (new_name, g.user['user_id']))

    # Sync student name if user is a student
    if g.user['role'] == 'student':
        execute("UPDATE students SET name = ? WHERE name = ?",
                (new_name, old_username))

    return jsonify({'message': '修改成功', 'username': new_name})


@auth_bp.route('/api/me/password', methods=['PUT'])
@login_required
def change_password():
    data = request.get_json()
    old_pw = data.get('old_password', '')
    new_pw = data.get('new_password', '')

    if not old_pw or not new_pw:
        return jsonify({'error': '新旧密码不能为空'}), 400
    if len(new_pw) < 6:
        return jsonify({'error': '新密码长度不能少于6位'}), 400

    user = query("SELECT * FROM users WHERE id = ?", (g.user['user_id'],), one=True)
    if not check_password_hash(user['password_hash'], old_pw):
        return jsonify({'error': '原密码错误'}), 400

    execute("UPDATE users SET password_hash = ? WHERE id = ?",
            (generate_password_hash(new_pw), g.user['user_id']))
    return jsonify({'message': '密码修改成功'})
