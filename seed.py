"""Seed script: populate the database with sample data."""
from werkzeug.security import generate_password_hash
from db import init_db, get_db, execute, query

init_db()

# Create users
users = [
    ('admin', generate_password_hash('admin123'), 'admin'),
    ('teacher', generate_password_hash('teacher123'), 'teacher'),
    ('student1', generate_password_hash('student123'), 'student'),
    ('student2', generate_password_hash('student123'), 'student'),
]
for u in users:
    existing = query("SELECT id FROM users WHERE username = ?", (u[0],))
    if not existing:
        execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", u)
print("Users seeded.")

# Create students
students = [
    ('2024001', '张三', '男', '计算机2401', '13800001001', 'zhangsan@example.com'),
    ('2024002', '李四', '女', '计算机2401', '13800001002', 'lisi@example.com'),
    ('2024003', '王五', '男', '软件2402', '13800001003', 'wangwu@example.com'),
    ('2024004', '赵六', '女', '软件2402', '13800001004', 'zhaoliu@example.com'),
    ('2024005', '孙七', '男', '大数据2403', '13800001005', 'sunqi@example.com'),
    ('2024006', 'student1', '男', '计算机2401', '13800001006', 'student1@example.com'),
    ('2024007', 'student2', '女', '软件2402', '13800001007', 'student2@example.com'),
]
student_ids = []
for s in students:
    existing = query("SELECT id FROM students WHERE student_no = ?", (s[0],))
    if not existing:
        sid = execute("INSERT INTO students (student_no, name, gender, class_name, phone, email) VALUES (?,?,?,?,?,?)", s)
        student_ids.append(sid)
    else:
        student_ids.append(existing[0]['id'])
print("Students seeded.")

# Create grades
grades = [
    (student_ids[0], '高等数学', 92, '2026春'),
    (student_ids[0], '大学英语', 85, '2026春'),
    (student_ids[0], '数据结构', 88, '2026春'),
    (student_ids[1], '高等数学', 76, '2026春'),
    (student_ids[1], '大学英语', 90, '2026春'),
    (student_ids[1], '数据结构', 82, '2026春'),
    (student_ids[2], '高等数学', 55, '2026春'),
    (student_ids[2], '大学英语', 68, '2026春'),
    (student_ids[2], '数据结构', 71, '2026春'),
    (student_ids[3], '高等数学', 88, '2026春'),
    (student_ids[3], '大学英语', 79, '2026春'),
    (student_ids[3], '数据结构', 94, '2026春'),
    (student_ids[4], '高等数学', 63, '2026春'),
    (student_ids[4], '大学英语', 72, '2026春'),
    (student_ids[4], '数据结构', 58, '2026春'),
    (student_ids[5], '高等数学', 80, '2026春'),
    (student_ids[5], '大学英语', 75, '2026春'),
    (student_ids[5], '数据结构', 82, '2026春'),
    (student_ids[6], '高等数学', 68, '2026春'),
    (student_ids[6], '大学英语', 91, '2026春'),
]
existing_grades = query("SELECT COUNT(*) as cnt FROM grades")
if existing_grades[0]['cnt'] == 0:
    for g in grades:
        execute("INSERT INTO grades (student_id, course_name, score, semester) VALUES (?,?,?,?)", g)
print("Grades seeded.")
print("Done! Default accounts: admin/admin123, teacher/teacher123, student1/student123")
