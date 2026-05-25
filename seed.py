"""Seed script: populate database with sample data."""
from werkzeug.security import generate_password_hash
from db import init_db, get_db, execute, query

init_db()

# Users
users = [
    ('admin', generate_password_hash('admin123'), 'admin'),
    ('teacher', generate_password_hash('teacher123'), 'teacher'),
]
for u in users:
    if not query("SELECT id FROM users WHERE username = ?", (u[0],)):
        execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)", u)
print("Users seeded.")

# Courses — comprehensive presets grouped by college
courses = [
    # 01 计算机科学与技术学院
    ('0101', '高等数学', '计算机科学与技术学院', '01'),
    ('0102', '线性代数', '计算机科学与技术学院', '01'),
    ('0103', '离散数学', '计算机科学与技术学院', '01'),
    ('0104', '数据结构', '计算机科学与技术学院', '01'),
    ('0105', '操作系统', '计算机科学与技术学院', '01'),
    ('0106', '计算机网络', '计算机科学与技术学院', '01'),
    ('0107', '数据库原理', '计算机科学与技术学院', '01'),
    ('0108', 'C语言程序设计', '计算机科学与技术学院', '01'),
    ('0109', 'Python程序设计', '计算机科学与技术学院', '01'),
    ('0110', 'Java程序设计', '计算机科学与技术学院', '01'),
    ('0111', '软件工程', '计算机科学与技术学院', '01'),
    ('0112', '编译原理', '计算机科学与技术学院', '01'),
    ('0113', '计算机组成原理', '计算机科学与技术学院', '01'),
    ('0114', '人工智能导论', '计算机科学与技术学院', '01'),
    ('0115', '算法设计与分析', '计算机科学与技术学院', '01'),

    # 02 数学与统计学院
    ('0201', '数学分析', '数学与统计学院', '02'),
    ('0202', '高等代数', '数学与统计学院', '02'),
    ('0203', '概率论与数理统计', '数学与统计学院', '02'),
    ('0204', '常微分方程', '数学与统计学院', '02'),
    ('0205', '数值分析', '数学与统计学院', '02'),
    ('0206', '运筹学', '数学与统计学院', '02'),
    ('0207', '应用统计学', '数学与统计学院', '02'),
    ('0208', '随机过程', '数学与统计学院', '02'),

    # 03 电子信息工程学院
    ('0301', '电路分析', '电子信息工程学院', '03'),
    ('0302', '模拟电子技术', '电子信息工程学院', '03'),
    ('0303', '数字电子技术', '电子信息工程学院', '03'),
    ('0304', '信号与系统', '电子信息工程学院', '03'),
    ('0305', '通信原理', '电子信息工程学院', '03'),
    ('0306', '电磁场与电磁波', '电子信息工程学院', '03'),
    ('0307', '嵌入式系统', '电子信息工程学院', '03'),
    ('0308', '自动控制原理', '电子信息工程学院', '03'),

    # 04 经济管理学院
    ('0401', '微观经济学', '经济管理学院', '04'),
    ('0402', '宏观经济学', '经济管理学院', '04'),
    ('0403', '管理学原理', '经济管理学院', '04'),
    ('0404', '会计学基础', '经济管理学院', '04'),
    ('0405', '市场营销', '经济管理学院', '04'),
    ('0406', '国际贸易实务', '经济管理学院', '04'),
    ('0407', '财务管理', '经济管理学院', '04'),
    ('0408', '人力资源管理', '经济管理学院', '04'),

    # 05 外国语学院
    ('0501', '综合英语', '外国语学院', '05'),
    ('0502', '英语听力', '外国语学院', '05'),
    ('0503', '英语口语', '外国语学院', '05'),
    ('0504', '英语写作', '外国语学院', '05'),
    ('0505', '日语基础', '外国语学院', '05'),
    ('0506', '翻译理论与实践', '外国语学院', '05'),
    ('0507', '英美文学', '外国语学院', '05'),
]
for c in courses:
    if not query("SELECT id FROM courses WHERE code = ?", (c[0],)):
        execute("INSERT INTO courses (code, name, college_name, college_code) VALUES (?,?,?,?)", c)
print(f"Courses seeded: {len(courses)}")

# Students — sample data with proper student_no format
students_data = [
    ('2401010112', '张三', '男', '2024', '01', '01', '计算机2401', '13800001001', 'zhangsan@example.com'),
    ('2401010123', '李四', '女', '2024', '01', '01', '计算机2401', '13800001002', 'lisi@example.com'),
    ('2401020214', '王五', '男', '2024', '01', '02', '软件2402', '13800001003', 'wangwu@example.com'),
    ('2401020215', '赵六', '女', '2024', '01', '02', '软件2402', '13800001004', 'zhaoliu@example.com'),
    ('2402030318', '孙七', '男', '2024', '02', '03', '统计2403', '13800001005', 'sunqi@example.com'),
    ('2403010409', 'student1', '男', '2024', '03', '01', '电子2401', '13800001006', 'student1@example.com'),
    ('2405010511', 'student2', '女', '2024', '05', '01', '英语2401', '13800001007', 'student2@example.com'),
]

student_ids = []
for s in students_data:
    existing = query("SELECT id FROM students WHERE student_no = ?", (s[0],))
    if not existing:
        sid = execute(
            "INSERT INTO students (student_no, name, gender, enrollment_year, college_code, major_code, class_name, phone, email) VALUES (?,?,?,?,?,?,?,?,?)",
            s
        )
        student_ids.append(sid)
        # Auto-create student user account
        if not query("SELECT id FROM users WHERE username = ?", (s[1],)):
            execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                    (s[1], generate_password_hash('Ad112233'), 'student'))
    else:
        student_ids.append(existing[0]['id'])
print(f"Students seeded: {len(student_ids)}")

# Grades — sample grades referencing courses
course_rows = query("SELECT id, code FROM courses")
course_map = {c['code']: c['id'] for c in course_rows}

grades_data = [
    (student_ids[0], '0101', 92, '2026', '一'),
    (student_ids[0], '0104', 88, '2026', '一'),
    (student_ids[0], '0108', 85, '2026', '一'),
    (student_ids[1], '0101', 76, '2026', '一'),
    (student_ids[1], '0104', 82, '2026', '一'),
    (student_ids[1], '0109', 90, '2026', '一'),
    (student_ids[2], '0101', 55, '2026', '一'),
    (student_ids[2], '0110', 68, '2026', '一'),
    (student_ids[2], '0111', 71, '2026', '一'),
    (student_ids[3], '0104', 88, '2026', '一'),
    (student_ids[3], '0105', 79, '2026', '一'),
    (student_ids[3], '0106', 94, '2026', '一'),
    (student_ids[4], '0201', 63, '2026', '一'),
    (student_ids[4], '0202', 72, '2026', '一'),
    (student_ids[4], '0203', 58, '2026', '一'),
    (student_ids[5], '0301', 80, '2026', '一'),
    (student_ids[5], '0302', 75, '2026', '一'),
    (student_ids[5], '0303', 82, '2026', '一'),
    (student_ids[6], '0501', 68, '2026', '一'),
    (student_ids[6], '0502', 91, '2026', '一'),
]

if not query("SELECT COUNT(*) as cnt FROM grades")[0]['cnt']:
    for g in grades_data:
        cid = course_map.get(g[1])
        if cid:
            execute("INSERT INTO grades (student_id, course_id, score, semester_year, semester_term) VALUES (?,?,?,?,?)",
                    (g[0], cid, g[2], g[3], g[4]))
print(f"Grades seeded: {len(grades_data)}")

print("\nDone! Accounts:")
print("  admin/admin123 | teacher/teacher123 | student1/Ad112233")
print("  All student accounts password: Ad112233")
