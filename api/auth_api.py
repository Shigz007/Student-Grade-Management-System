from flask import Blueprint, request, jsonify, g
from werkzeug.security import check_password_hash
from auth import create_token, login_required
from db import query

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
