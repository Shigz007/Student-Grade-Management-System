"""Seed script: populate both databases with fresh sample data."""
import os
import random
from werkzeug.security import generate_password_hash
from config import SCHOOL_DATABASE
from db import init_db, execute, query

# Clean start for school DB
if os.path.exists(SCHOOL_DATABASE):
    try:
        os.remove(SCHOOL_DATABASE)
    except OSError:
        pass

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

# Colleges
colleges_data = [
    ('01', '计算机科学与技术学院'),
    ('02', '数学与统计学院'),
    ('03', '电子信息工程学院'),
    ('04', '经济管理学院'),
    ('05', '外国语学院'),
    ('06', '机械工程学院'),
    ('07', '土木工程学院'),
    ('08', '化学与化工学院'),
    ('09', '法学院'),
    ('10', '医学院'),
    ('11', '文学院'),
]
for code, name in colleges_data:
    if not query("SELECT code FROM colleges WHERE code = ?", (code,)):
        execute("INSERT INTO colleges (code, name) VALUES (?, ?)", (code, name))
print(f"Colleges seeded: {len(colleges_data)}")

# Majors
majors_data = [
    ('01', '01', '计算机科学与技术'),
    ('01', '02', '软件工程'),
    ('01', '03', '信息安全'),
    ('02', '01', '数学与应用数学'),
    ('02', '02', '统计学'),
    ('03', '01', '电子信息工程'),
    ('03', '02', '通信工程'),
    ('03', '03', '光电信息科学与工程'),
    ('04', '01', '经济学'),
    ('04', '02', '工商管理'),
    ('04', '03', '会计学'),
    ('05', '01', '英语'),
    ('05', '02', '日语'),
    ('05', '03', '翻译'),
    ('06', '01', '机械工程'),
    ('06', '02', '车辆工程'),
    ('07', '01', '土木工程'),
    ('07', '02', '建筑学'),
    ('08', '01', '化学'),
    ('08', '02', '化学工程与工艺'),
    ('09', '01', '法学'),
    ('09', '02', '知识产权'),
    ('10', '01', '临床医学'),
    ('10', '02', '护理学'),
    ('11', '01', '汉语言文学'),
    ('11', '02', '新闻学'),
    ('11', '03', '历史学'),
    ('11', '04', '广告学'),
]
for col_code, maj_code, maj_name in majors_data:
    if not query("SELECT id FROM majors WHERE college_code = ? AND code = ?", (col_code, maj_code)):
        execute("INSERT INTO majors (college_code, code, name) VALUES (?, ?, ?)",
                (col_code, maj_code, maj_name))
print(f"Majors seeded: {len(majors_data)}")

# Courses — (code, name, college_code, major_code)
courses = [
    # 01 计算机科学与技术学院
    ('0101', '高等数学', '01', '01'),
    ('0102', '线性代数', '01', '01'),
    ('0103', '离散数学', '01', '01'),
    ('0104', '数据结构', '01', '01'),
    ('0105', '操作系统', '01', '01'),
    ('0106', '计算机网络', '01', '01'),
    ('0107', '数据库原理', '01', '01'),
    ('0108', 'C语言程序设计', '01', '01'),
    ('0109', 'Python程序设计', '01', '01'),
    ('0110', '计算机组成原理', '01', '01'),
    ('0111', '编译原理', '01', '01'),
    ('0112', '算法设计与分析', '01', '01'),
    ('0113', '人工智能导论', '01', '01'),
    ('0114', '数字逻辑', '01', '01'),
    ('0115', '计算机图形学', '01', '01'),
    ('0116', '软件工程概论', '01', '02'),
    ('0117', '面向对象程序设计', '01', '02'),
    ('0118', 'Java程序设计', '01', '02'),
    ('0119', '软件需求分析', '01', '02'),
    ('0120', '软件测试', '01', '02'),
    ('0121', '软件项目管理', '01', '02'),
    ('0122', 'Web前端开发', '01', '02'),
    ('0123', '移动应用开发', '01', '02'),
    ('0124', '软件架构设计', '01', '02'),
    ('0125', 'Linux系统管理', '01', '02'),
    ('0126', '信息安全基础', '01', '03'),
    ('0127', '密码学', '01', '03'),
    ('0128', '网络安全', '01', '03'),
    ('0129', '系统安全', '01', '03'),
    ('0130', '恶意代码分析', '01', '03'),

    # 02 数学与统计学院
    ('0201', '数学分析', '02', '01'),
    ('0202', '高等代数', '02', '01'),
    ('0203', '概率论与数理统计', '02', '01'),
    ('0204', '常微分方程', '02', '01'),
    ('0205', '数值分析', '02', '01'),
    ('0206', '运筹学', '02', '01'),
    ('0207', '复变函数', '02', '01'),
    ('0208', '实变函数', '02', '01'),
    ('0209', '泛函分析', '02', '01'),
    ('0210', '偏微分方程', '02', '01'),
    ('0211', '图论', '02', '01'),
    ('0212', '抽象代数', '02', '01'),
    ('0213', '拓扑学', '02', '01'),
    ('0214', '应用统计学', '02', '02'),
    ('0215', '随机过程', '02', '02'),
    ('0216', '多元统计分析', '02', '02'),
    ('0217', '时间序列分析', '02', '02'),
    ('0218', '抽样调查', '02', '02'),
    ('0219', '统计计算', '02', '02'),
    ('0220', '数据挖掘', '02', '02'),
    ('0221', '回归分析', '02', '02'),

    # 03 电子信息工程学院
    ('0301', '电路分析', '03', '01'),
    ('0302', '模拟电子技术', '03', '01'),
    ('0303', '数字电子技术', '03', '01'),
    ('0304', '信号与系统', '03', '01'),
    ('0305', '电磁场与电磁波', '03', '01'),
    ('0306', '嵌入式系统', '03', '01'),
    ('0307', '自动控制原理', '03', '01'),
    ('0308', '数字信号处理', '03', '01'),
    ('0309', '微机原理', '03', '01'),
    ('0310', '传感器技术', '03', '01'),
    ('0311', '电子测量', '03', '01'),
    ('0312', '通信原理', '03', '02'),
    ('0313', '信息论基础', '03', '02'),
    ('0314', '移动通信', '03', '02'),
    ('0315', '光纤通信', '03', '02'),
    ('0316', '卫星通信', '03', '02'),
    ('0317', '微波技术与天线', '03', '02'),
    ('0318', '数字图像处理', '03', '02'),
    ('0319', '光电子学', '03', '03'),
    ('0320', '激光原理', '03', '03'),
    ('0321', '光电检测技术', '03', '03'),
    ('0322', '光纤传感技术', '03', '03'),

    # 04 经济管理学院
    ('0401', '微观经济学', '04', '01'),
    ('0402', '宏观经济学', '04', '01'),
    ('0403', '计量经济学', '04', '01'),
    ('0404', '国际经济学', '04', '01'),
    ('0405', '会计学基础', '04', '01'),
    ('0406', '发展经济学', '04', '01'),
    ('0407', '产业经济学', '04', '01'),
    ('0408', '财政学', '04', '01'),
    ('0409', '金融学', '04', '01'),
    ('0410', '管理学原理', '04', '02'),
    ('0411', '市场营销', '04', '02'),
    ('0412', '人力资源管理', '04', '02'),
    ('0413', '国际贸易实务', '04', '02'),
    ('0414', '战略管理', '04', '02'),
    ('0415', '组织行为学', '04', '02'),
    ('0416', '运营管理', '04', '02'),
    ('0417', '企业伦理', '04', '02'),
    ('0418', '中级财务会计', '04', '03'),
    ('0419', '成本会计', '04', '03'),
    ('0420', '审计学', '04', '03'),
    ('0421', '财务管理', '04', '03'),
    ('0422', '税务筹划', '04', '03'),

    # 05 外国语学院
    ('0501', '综合英语', '05', '01'),
    ('0502', '英语听力', '05', '01'),
    ('0503', '英语口语', '05', '01'),
    ('0504', '英语写作', '05', '01'),
    ('0505', '翻译理论与实践', '05', '01'),
    ('0506', '英美文学', '05', '01'),
    ('0507', '语言学概论', '05', '01'),
    ('0508', '跨文化交际', '05', '01'),
    ('0509', '第二外语（日语）', '05', '01'),
    ('0510', '英语演讲', '05', '01'),
    ('0511', '日语基础', '05', '02'),
    ('0512', '日语听力', '05', '02'),
    ('0513', '日语口语', '05', '02'),
    ('0514', '日语写作', '05', '02'),
    ('0515', '日本文学', '05', '02'),
    ('0516', '商务日语', '05', '02'),
    ('0517', '日本文化', '05', '02'),
    ('0518', '口译基础', '05', '03'),
    ('0519', '笔译实务', '05', '03'),
    ('0520', '交替传译', '05', '03'),
    ('0521', '科技翻译', '05', '03'),
    ('0522', '商务翻译', '05', '03'),

    # 06 机械工程学院
    ('0601', '工程力学', '06', '01'),
    ('0602', '机械制图', '06', '01'),
    ('0603', '机械设计', '06', '01'),
    ('0604', '机械制造基础', '06', '01'),
    ('0605', '工程材料', '06', '01'),
    ('0606', '液压与气动', '06', '01'),
    ('0607', '数控技术', '06', '01'),
    ('0608', '机械原理', '06', '01'),
    ('0609', '热力学', '06', '01'),
    ('0610', '流体力学', '06', '01'),
    ('0611', 'CAD/CAM技术', '06', '01'),
    ('0612', '汽车构造', '06', '02'),
    ('0613', '发动机原理', '06', '02'),
    ('0614', '汽车电子控制', '06', '02'),
    ('0615', '新能源汽车技术', '06', '02'),
    ('0616', '汽车设计', '06', '02'),
    ('0617', '汽车试验学', '06', '02'),

    # 07 土木工程学院
    ('0701', '理论力学', '07', '01'),
    ('0702', '材料力学', '07', '01'),
    ('0703', '结构力学', '07', '01'),
    ('0704', '混凝土结构', '07', '01'),
    ('0705', '钢结构', '07', '01'),
    ('0706', '土力学', '07', '01'),
    ('0707', '工程测量', '07', '01'),
    ('0708', '施工技术', '07', '01'),
    ('0709', '基础工程', '07', '01'),
    ('0710', '桥梁工程', '07', '01'),
    ('0711', '道路工程', '07', '01'),
    ('0712', '工程地质', '07', '01'),
    ('0713', '建筑设计', '07', '02'),
    ('0714', '建筑历史', '07', '02'),
    ('0715', '建筑物理', '07', '02'),
    ('0716', '城市规划原理', '07', '02'),
    ('0717', '建筑构造', '07', '02'),
    ('0718', '景观设计', '07', '02'),

    # 08 化学与化工学院
    ('0801', '无机化学', '08', '01'),
    ('0802', '有机化学', '08', '01'),
    ('0803', '分析化学', '08', '01'),
    ('0804', '物理化学', '08', '01'),
    ('0805', '高分子化学', '08', '01'),
    ('0806', '仪器分析', '08', '01'),
    ('0807', '结构化学', '08', '01'),
    ('0808', '生物化学', '08', '01'),
    ('0809', '环境化学', '08', '01'),
    ('0810', '化工原理', '08', '02'),
    ('0811', '化学反应工程', '08', '02'),
    ('0812', '化工热力学', '08', '02'),
    ('0813', '分离工程', '08', '02'),
    ('0814', '化工工艺学', '08', '02'),
    ('0815', '催化原理', '08', '02'),
    ('0816', '化工安全与环保', '08', '02'),

    # 09 法学院
    ('0901', '法理学', '09', '01'),
    ('0902', '宪法学', '09', '01'),
    ('0903', '民法学', '09', '01'),
    ('0904', '刑法学', '09', '01'),
    ('0905', '行政法学', '09', '01'),
    ('0906', '经济法学', '09', '01'),
    ('0907', '国际法', '09', '01'),
    ('0908', '民事诉讼法', '09', '01'),
    ('0909', '刑事诉讼法', '09', '01'),
    ('0910', '商法学', '09', '01'),
    ('0911', '环境资源法', '09', '01'),
    ('0912', '劳动与社会保障法', '09', '01'),
    ('0913', '知识产权法', '09', '02'),
    ('0914', '专利法', '09', '02'),
    ('0915', '商标法', '09', '02'),
    ('0916', '著作权法', '09', '02'),
    ('0917', '知识产权管理', '09', '02'),

    # 10 医学院
    ('1001', '人体解剖学', '10', '01'),
    ('1002', '生理学', '10', '01'),
    ('1003', '病理学', '10', '01'),
    ('1004', '药理学', '10', '01'),
    ('1005', '内科学', '10', '01'),
    ('1006', '外科学', '10', '01'),
    ('1007', '诊断学', '10', '01'),
    ('1008', '医学影像学', '10', '01'),
    ('1009', '妇产科学', '10', '01'),
    ('1010', '儿科学', '10', '01'),
    ('1011', '传染病学', '10', '01'),
    ('1012', '神经病学', '10', '01'),
    ('1013', '护理学基础', '10', '02'),
    ('1014', '内科护理学', '10', '02'),
    ('1015', '外科护理学', '10', '02'),
    ('1016', '妇产科护理学', '10', '02'),
    ('1017', '儿科护理学', '10', '02'),
    ('1018', '社区护理学', '10', '02'),

    # 11 文学院
    ('1101', '中国古代文学', '11', '01'),
    ('1102', '中国现当代文学', '11', '01'),
    ('1103', '外国文学', '11', '01'),
    ('1104', '文学理论', '11', '01'),
    ('1105', '古代汉语', '11', '01'),
    ('1106', '现代汉语', '11', '01'),
    ('1107', '语言学概论', '11', '01'),
    ('1108', '写作学', '11', '01'),
    ('1109', '比较文学', '11', '01'),
    ('1110', '中国古典文献学', '11', '01'),
    ('1111', '民间文学', '11', '01'),
    ('1112', '文艺美学', '11', '01'),
    ('1113', '新闻学概论', '11', '02'),
    ('1114', '传播学', '11', '02'),
    ('1115', '新闻采访与写作', '11', '02'),
    ('1116', '新闻编辑', '11', '02'),
    ('1117', '新闻评论', '11', '02'),
    ('1118', '广播电视新闻学', '11', '02'),
    ('1119', '新媒体概论', '11', '02'),
    ('1120', '媒介伦理与法规', '11', '02'),
    ('1121', '中国通史', '11', '03'),
    ('1122', '世界通史', '11', '03'),
    ('1123', '史学概论', '11', '03'),
    ('1124', '考古学通论', '11', '03'),
    ('1125', '历史文献学', '11', '03'),
    ('1126', '中国近代史', '11', '03'),
    ('1127', '专门史', '11', '03'),
    ('1128', '历史地理学', '11', '03'),
    ('1129', '广告学概论', '11', '04'),
    ('1130', '广告策划与创意', '11', '04'),
    ('1131', '广告文案写作', '11', '04'),
    ('1132', '品牌传播', '11', '04'),
    ('1133', '市场营销学', '11', '04'),
    ('1134', '消费者行为学', '11', '04'),
    ('1135', '视觉传达设计', '11', '04'),
]
for c in courses:
    if not query("SELECT id FROM courses WHERE code = ?", (c[0],)):
        execute("INSERT INTO courses (code, name, college_code, major_code) VALUES (?,?,?,?)", c)
print(f"Courses seeded: {len(courses)}")

# Fresh random Chinese names
SURNAMES = ['王', '李', '张', '刘', '陈', '杨', '黄', '赵', '吴', '周', '徐', '孙', '马', '朱', '胡', '林', '郭', '何', '高', '罗',
            '郑', '梁', '谢', '宋', '唐', '许', '韩', '冯', '邓', '曹', '彭', '曾', '萧', '田', '董', '潘', '袁', '蔡', '蒋', '余',
            '于', '杜', '叶', '程', '苏', '魏', '吕', '丁', '任', '沈', '姚', '卢', '姜', '崔', '钟', '谭', '陆', '汪', '范', '金',
            '石', '方', '白', '秦', '段', '江', '史', '侯', '龙', '万', '雷', '钱', '汤', '尹', '易', '常', '武', '乔', '贺', '赖',
            '龚', '文', '康', '毛', '邱', '向', '廖', '邹', '熊', '孟', '戴', '夏', '薛', '邵', '傅', '汪', '贾', '阎', '郝', '孔']
GIVEN_MALE = ['伟', '强', '磊', '军', '勇', '杰', '涛', '明', '辉', '鹏', '浩', '峰', '宇', '轩', '文', '博', '超', '毅', '晨', '睿',
              '飞', '彬', '豪', '哲', '恒', '诚', '安', '宁', '龙', '威', '阳', '志', '健', '凯', '俊', '刚', '亮', '平', '翔', '斌',
              '松', '霖', '旭', '川', '震', '坤', '裕', '楠', '良', '成', '庆', '彦', '宏', '建', '家', '友', '德', '兴', '永', '源']
GIVEN_FEMALE = ['芳', '敏', '静', '丽', '婷', '雪', '琳', '玲', '瑶', '颖', '娜', '莉', '娟', '霞', '萍', '红', '梅', '洁', '蓉', '燕',
                '怡', '欣', '雨', '思', '文', '瑜', '婉', '悦', '蕾', '菲', '兰', '慧', '云', '佳', '秀', '晶', '馨', '月', '凤', '珠',
                '巧', '美', '露', '婵', '姬', '环', '翠', '芬', '芝', '娥', '淑', '惠', '丹', '君', '筠', '艳', '彩', '春', '秋', '碧']

_used_names = set()

def random_name():
    for _ in range(1000):
        surname = random.choice(SURNAMES)
        gender_roll = random.random()
        if gender_roll < 0.48:
            given = random.choice(GIVEN_MALE)
            gender = '男'
        elif gender_roll < 0.93:
            given = random.choice(GIVEN_FEMALE)
            gender = '女'
        else:
            name_pool = ['子涵', '梓轩', '雨桐', '浩然', '一鸣', '天佑', '俊杰', '思远', '乐天', '逸飞',
                        '星辰', '沐阳', '若兮', '瑾瑜', '知行', '修远', '明哲', '致远', '承志', '凌云']
            given = random.choice(name_pool)
            gender = random.choice(['男', '女'])
        full = surname + given
        if full not in _used_names:
            _used_names.add(full)
            return full, gender
    # Fallback: append a digit
    surname = random.choice(SURNAMES)
    given = random.choice(GIVEN_MALE + GIVEN_FEMALE)
    full = surname + given + str(random.randint(1, 99))
    _used_names.add(full)
    return full, random.choice(['男', '女'])

# Generate students across all colleges and majors
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

college_majors = {
    '01': ['01', '02', '03'],
    '02': ['01', '02'],
    '03': ['01', '02', '03'],
    '04': ['01', '02', '03'],
    '05': ['01', '02', '03'],
    '06': ['01', '02'],
    '07': ['01', '02'],
    '08': ['01', '02'],
    '09': ['01', '02'],
    '10': ['01', '02'],
    '11': ['01', '02', '03', '04'],
}

# Generate students across all colleges and majors
RANDOM_SEED = 42
random.seed(RANDOM_SEED)

college_majors = {
    '01': ['01', '02', '03'],
    '02': ['01', '02'],
    '03': ['01', '02', '03'],
    '04': ['01', '02', '03'],
    '05': ['01', '02', '03'],
    '06': ['01', '02'],
    '07': ['01', '02'],
    '08': ['01', '02'],
    '09': ['01', '02'],
    '10': ['01', '02'],
    '11': ['01', '02', '03', '04'],
}

DEFAULT_STUDENT_PASSWORD = 'Ad112233'

# Build class list: (college_code, major_code, class_name)
all_classes = []
for college_code, majors in college_majors.items():
    for major_code in majors:
        # 2 classes per major
        for cls_seq in range(1, 3):
            cls_name = str(cls_seq).zfill(2)
            all_classes.append((college_code, major_code, cls_name))

print(f"Total classes to generate: {len(all_classes)}")

student_records = []
for college_code, major_code, class_name in all_classes:
    num_students = random.randint(25, 35)
    for seq in range(1, num_students + 1):
        student_no = f'24{college_code}{major_code}{class_name}{str(seq).zfill(2)}'
        name, gender = random_name()
        phone = f'138{random.randint(10000000, 99999999)}'
        student_records.append((student_no, name, gender, '2024', college_code, major_code, class_name, phone))

random.shuffle(student_records)

student_ids = []
for s in student_records:
    if not query("SELECT id FROM students WHERE student_no = ?", (s[0],)):
        if not query("SELECT id FROM users WHERE username = ?", (s[1],)):
            uid = execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                          (s[1], generate_password_hash(DEFAULT_STUDENT_PASSWORD), 'student'))
        else:
            uid = query("SELECT id FROM users WHERE username = ?", (s[1],), one=True)['id']
        sid = execute(
            "INSERT INTO students (student_no, name, gender, enrollment_year, college_code, major_code, class_name, phone, email, user_id) "
            "VALUES (?,?,?,?,?,?,?,?,?,?)",
            (s[0], s[1], s[2], s[3], s[4], s[5], s[6], s[7], '', uid)
        )
        student_ids.append(sid)
    else:
        existing = query("SELECT id FROM students WHERE student_no = ?", (s[0],))
        student_ids.append(existing[0]['id'])
print(f"Students seeded: {len(student_ids)}")

# ===== Teachers =====
TEACHER_NAMES = [
    ('张教授', 'TcAb12X'), ('李老师', 'TcCd34Y'), ('王导师', 'TcEf56Z'),
    ('刘教授', 'TcGh78A'), ('陈老师', 'TcIj90B'), ('杨老师', 'TcKl12C'),
    ('黄教授', 'TcMn34D'), ('赵老师', 'TcOp56E'), ('周导师', 'TcQr78F'),
    ('吴教授', 'TcSt90G'), ('徐老师', 'TcUv12H'), ('孙老师', 'TcWx34I'),
    ('马教授', 'TcYz56J'), ('胡老师', 'TcAb78K'), ('林老师', 'TcCd90L'),
    ('郭教授', 'TcEf12M'), ('何老师', 'TcGh34N'), ('高导师', 'TcIj56O'),
    ('罗教授', 'TcKl78P'), ('郑老师', 'TcMn90Q'), ('梁老师', 'TcOp12R'),
    ('谢教授', 'TcQr34S'), ('宋老师', 'TcSt56T'), ('唐导师', 'TcUv78U'),
    ('韩教授', 'TcWx90V'), ('冯老师', 'TcYz12W'), ('邓老师', 'TcAb34X'),
    ('曹教授', 'TcCd56Y'), ('彭老师', 'TcEf78Z'), ('曾导师', 'TcGh90M'),
]

# Assign each teacher 2-5 classes from across the system
teacher_class_assignments = []  # (teacher_name, college_code, major_code, class_name)
remaining_classes = list(all_classes)
random.shuffle(remaining_classes)

for i, (tname, tpwd) in enumerate(TEACHER_NAMES):
    num_classes = min(random.randint(2, 5), len(remaining_classes))
    if num_classes < 1:
        num_classes = random.randint(2, 5)
        assigned = random.sample(all_classes, min(num_classes, len(all_classes)))
    else:
        assigned = remaining_classes[:num_classes]
        remaining_classes = remaining_classes[num_classes:]
    for cls in assigned:
        teacher_class_assignments.append((tname, cls[0], cls[1], cls[2]))

teacher_count = 0
for tname, tpwd in TEACHER_NAMES:
    if not query("SELECT id FROM users WHERE username = ?", (tname,)):
        uid = execute("INSERT INTO users (username, password_hash, role) VALUES (?,?,?)",
                      (tname, generate_password_hash(tpwd), 'teacher'))
        teacher_count += 1
    else:
        uid = query("SELECT id FROM users WHERE username = ?", (tname,), one=True)['id']

    for _, cc, mc, cn in teacher_class_assignments:
        if _ == tname:
            if not query("SELECT id FROM teacher_classes WHERE user_id = ? AND college_code = ? AND major_code = ? AND class_name = ?",
                        (uid, cc, mc, cn)):
                execute("INSERT INTO teacher_classes (user_id, college_code, major_code, class_name) VALUES (?,?,?,?)",
                        (uid, cc, mc, cn))

print(f"Teachers seeded: {teacher_count}")
print(f"Teacher-class assignments: {len(teacher_class_assignments)}")

# ===== Schedules =====
# For each class that has a teacher, generate a weekly schedule
TIME_SLOTS = 6  # 1-6
DAYS = 5  # 1-5

schedule_count = 0
for tname, college_code, major_code, class_name in teacher_class_assignments:
    # Check if schedule already exists for this class
    existing = query(
        "SELECT COUNT(*) as cnt FROM schedules WHERE college_code = ? AND major_code = ? AND class_name = ?",
        (college_code, major_code, class_name)
    )
    if existing[0]['cnt'] > 0:
        continue

    # Get courses for this major
    major_courses = query(
        "SELECT id, code, name FROM courses WHERE college_code = ? AND major_code = ?",
        (college_code, major_code)
    )
    if not major_courses:
        continue

    # Build schedule: fill ~60-80% of slots (5 days × 4-5 slots per day)
    # We limit to time_slots 1-5 for most (slot 6 is evening, fewer classes)
    filled = 0
    for day in range(1, DAYS + 1):
        # Each day has ~3-5 courses
        day_slots = random.sample(range(1, 6), random.randint(3, 5))
        for slot in day_slots:
            course = random.choice(major_courses)
            if not query(
                "SELECT id FROM schedules WHERE college_code = ? AND major_code = ? AND class_name = ? AND day_of_week = ? AND time_slot = ?",
                (college_code, major_code, class_name, day, slot)
            ):
                execute(
                    "INSERT INTO schedules (college_code, major_code, class_name, day_of_week, time_slot, course_id) VALUES (?,?,?,?,?,?)",
                    (college_code, major_code, class_name, day, slot, course['id'])
                )
                filled += 1

    schedule_count += filled

print(f"Schedule entries seeded: {schedule_count}")

# ===== Grades =====
# Group courses by (college_code, major_code) for major-specific assignment
course_rows = query("SELECT id, code, college_code, major_code FROM courses")
course_by_major = {}
for c in course_rows:
    course_by_major.setdefault((c['college_code'], c['major_code']), []).append(c)

grade_count = 0
student_rows = query("SELECT id, student_no, college_code, major_code FROM students")
semester_years = ['2025', '2026']
semester_terms = ['一', '二']

for student in student_rows:
    sid = student['id']
    available = course_by_major.get((student['college_code'], student['major_code']), [])
    if not available:
        continue
    # Assign grade for EVERY course in this student's major
    for course in available:
        if not query("SELECT id FROM grades WHERE student_id = ? AND course_id = ?",
                     (sid, course['id'])):
            score = round(random.gauss(72, 16), 1)
            score = max(0, min(100, score))
            sy = random.choice(semester_years)
            st = random.choice(semester_terms)
            execute(
                "INSERT INTO grades (student_id, course_id, score, semester_year, semester_term) VALUES (?,?,?,?,?)",
                (sid, course['id'], score, sy, st)
            )
            grade_count += 1

print(f"Grades seeded: {grade_count}")

user_count = query("SELECT COUNT(*) as cnt FROM users")[0]['cnt']
teacher_class_count = query("SELECT COUNT(*) as cnt FROM teacher_classes")[0]['cnt']
schedule_entry_count = query("SELECT COUNT(*) as cnt FROM schedules")[0]['cnt']
print(f"\n=== Seed Complete ===")
print(f"Users: {user_count}")
print(f"Students: {len(student_ids)}")
print(f"Teachers: {teacher_count}")
print(f"Teacher-Class assignments: {teacher_class_count}")
print(f"Schedule entries: {schedule_entry_count}")
print(f"Grades: {grade_count}")
print(f"Classes: {len(all_classes)}")
print(f"\nAdmin: admin/admin123")
print(f"Demo Teacher: teacher/teacher123")
print(f"All student passwords: {DEFAULT_STUDENT_PASSWORD}")
for tname, tpwd in TEACHER_NAMES[:3]:
    print(f"Teacher: {tname}/{tpwd}")
