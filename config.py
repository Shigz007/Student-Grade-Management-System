import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'data.db')
SECRET_KEY = 'student-grade-system-secret-key-2026'
JWT_ALGORITHM = 'HS256'
