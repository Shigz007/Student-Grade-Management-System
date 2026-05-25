import jwt
import datetime
from functools import wraps
from flask import request, jsonify, g
from config import SECRET_KEY, JWT_ALGORITHM
from db import query


def create_token(user_id, username, role):
    payload = {
        'user_id': user_id,
        'username': username,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': '请先登录'}), 401
        payload = verify_token(token)
        if not payload:
            return jsonify({'error': '登录已过期，请重新登录'}), 401
        g.user = payload
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if g.user['role'] != 'admin':
            return jsonify({'error': '权限不足'}), 403
        return f(*args, **kwargs)
    return decorated


def teacher_or_admin(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if g.user['role'] not in ('admin', 'teacher'):
            return jsonify({'error': '权限不足'}), 403
        return f(*args, **kwargs)
    return decorated
