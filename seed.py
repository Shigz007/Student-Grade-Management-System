"""Seed script: populate database with fresh random sample data."""
import random
from werkzeug.security import generate_password_hash
from db import init_db, execute, query

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

# Fresh random Chinese names
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周', '徐', '孙', '马', '朱', '胡', '林', '郭', '何', '高', '罗',
            '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹', '彭', '曾', '萧', '田', '董', '潘', '袁', '蔡', '蒋', '余',
            '于', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈', '姚', '卢', '姜', '崔', '钟', '谭', '陆', '汪', '范', '金']
GIVEN_MALE = ['伟', '强', '磊', '军', '勇', '杰', '涛', '明', '辉', '鹏', '浩', '峰', '宇', '轩', '文', '博', '超', '毅', '晨', '睿',
              '飞', '彬', '豪', '哲', '恒', '诚', '安', '宁', '龙', '威', '阳', '志', '健', '凯', '俊', '刚', '亮', '平', '毅', '翔']
GIVEN_FEMALE = ['芳', '敏', '静', '丽', '婷', '雪', '琳', '玲', '瑶', '颖', '娜', '莉', '娟', '霞', '萍', '红', '梅', '洁', '蓉', '燕',
                '婷', '怡', '欣', '雨', '思', '文', '瑜', '婉', '悦', '蕾', '菲', '兰', '慧', '云', '佳', '秀', '晶', '馨', '月', '凤']
GIVEN_NEUTRAL = ['子涵', '梓轩', '雨桐', '浩然', '一鸣', '天佑', '俊杰', '思远', '乐天', '逸飞', '星辰', '沐阳', '若兮', '瑾瑜', '知行',
                 '修远', '明哲', '致远', '承志', '凌云', '瑞霖', '玉泽', '景行', '怀瑾', '握瑜', '含章', '贞元', '颖川', '建安', '元亮']

def random_name():
    surname = random.choice(SURNAMES)
    gender_roll = random.random()
    if gender_roll < 0.45:
        given = random.choice(GIVEN_MALE)
        gender = '男'
    elif gender_roll < 0.9:
        given = random.choice(GIVEN_FEMALE)
        gender = '女'
    else:
        given = random.choice(GIVEN_NEUTRAL)
        gender = random.choice(['男', '女'])
    return surname + given, gender

# Generate students across 5 colleges, 2 majors each, multiple classes
# Year: 2024, class sizes vary from 8 to 45
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

college_majors = {
    '01': ['01', '02'],  # 计算机, 软件
    '02': ['01', '02'],  # 数学, 统计
    '03': ['01', '02'],  # 电子, 通信
    '04': ['01', '02'],  # 经济, 管理
    '05': ['01', '02'],  # 英语, 日语
}

student_records = []
for college_code, majors in college_majors.items():
    for major_code in majors:
        # Each major gets 1-3 classes with 8-45 students each
        num_classes = random.randint(1, 3)
        for class_seq in range(1, num_classes + 1):
            cls = str(class_seq).zfill(2)
            num_students = random.randint(8, 45)
            for seq in range(1, num_students + 1):
                student_no = f'24{college_code}{major_code}{cls}{str(seq).zfill(2)}'
                name, gender = random_name()
                phone = f'138{random.randint(10000000, 99999999)}'
                student_records.append((student_no, name, gender, '2024', college_code, major_code, phone))

# Shuffle to avoid clustering
random.shuffle(student_records)

student_ids = []
for s in student_records:
    if not query("SELECT id FROM students WHERE student_no = ?", (s[0],)):
        sid = execute(
            "INSERT INTO students (student_no, name, gender, enrollment_year, college_code, major_code, class_name, phone, email) "
            "VALUES (?,?,?,?,?,?,?,?,?)",
            (s[0], s[1], s[2], s[3], s[4], s[5], '', s[6], '')
        )
        student_ids.append(sid)
        # Auto-create student user account
        if not query("SELECT id FROM users WHERE username = ?", (s[1],)):
            execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                    (s[1], generate_password_hash('Ad112233'), 'student'))
    else:
        existing = query("SELECT id FROM students WHERE student_no = ?", (s[0],))
        student_ids.append(existing[0]['id'])
print(f"Students seeded: {len(student_ids)}")

# Generate grades — each student gets 3-6 random courses from their college
course_rows = query("SELECT id, code, college_code FROM courses")
course_by_college = {}
for c in course_rows:
    course_by_college.setdefault(c['college_code'], []).append(c)

grade_count = 0
student_rows = query("SELECT id, student_no, college_code FROM students")
semester_years = ['2025', '2026']
semester_terms = ['一', '二']

for student in student_rows:
    sid = student['id']
    college = student['student_no'][2:4]  # college_code from student_no
    available = course_by_college.get(college, [])
    if not available:
        continue
    # Pick 3-6 random courses
    num_courses = random.randint(3, min(6, len(available)))
    chosen = random.sample(available, num_courses)
    for course in chosen:
        if not query("SELECT id FROM grades WHERE student_id = ? AND course_id = ?",
                     (sid, course['id'])):
            score = round(random.gauss(72, 16), 1)
            score = max(0, min(100, score))  # Clamp 0-100
            sy = random.choice(semester_years)
            st = random.choice(semester_terms)
            execute(
                "INSERT INTO grades (student_id, course_id, score, semester_year, semester_term) VALUES (?,?,?,?,?)",
                (sid, course['id'], score, sy, st)
            )
            grade_count += 1
print(f"Grades seeded: {grade_count}")

# Print summary
user_count = query("SELECT COUNT(*) as cnt FROM users")[0]['cnt']
print(f"\nDone! Total users: {user_count}, Students: {len(student_ids)}, Grades: {grade_count}")
print("Accounts: admin/admin123 | teacher/teacher123")
print("All student accounts password: Ad112233")
