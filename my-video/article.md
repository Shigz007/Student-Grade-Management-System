# 学生成绩管理系统 — 系统介绍

## 这是什么

一个基于 Flask + SQLite 的 Web 学生成绩管理系统，采用前后端分离架构，支持管理员、教师、学生三种角色，具备 JWT 认证、成绩录入查询统计、学生管理、仪表盘展示等完整功能。系统内置 11 个学院、28 个专业、238 门课程、1729 名学生，开箱即用，适合高校教学管理场景。

## 系统架构

### 后端技术栈

- **Web 框架**：Flask，轻量级 Python Web 框架
- **数据库**：SQLite，双数据库架构（data.db 存放用户/学生/成绩数据，school.db 存放学院/专业/课程数据）
- **认证**：JWT（JSON Web Token），Bearer Token 方案，HS256 算法签名
- **API 风格**：RESTful，Blueprint 模块化路由
- **跨库查询**：SQLite ATTACH DATABASE 机制，两个数据库通过一次连接完成跨库 JOIN

### 前端技术栈

- **UI 框架**：Bootstrap 4 + jQuery
- **UI Kit**：Boomerang Bootstrap 4 UI Kit
- **图表库**：ApexCharts.js（仪表盘柱状图/饼图）
- **架构**：前后端分离，模板直接渲染，API 通过 jQuery AJAX 调用

### 双数据库设计

| 数据库 | 文件 | 内容 |
|--------|------|------|
| 主数据库 | data.db | users（用户表）、students（学生表）、grades（成绩表） |
| 学校数据库 | school.db | colleges（学院表）、majors（专业表）、courses（课程表） |

通过 `ATTACH DATABASE 'school.db' AS school` 在主数据库连接上挂载学校数据库，成绩查询可直接 JOIN students、courses、colleges 三张跨库表，一条 SQL 完成学号、姓名、课程名、学院名、成绩、学期的联合查询。

```sql
SELECT s.student_no, s.name, c.name as course_name, cl.name as college_name,
       g.score, g.semester_year, g.semester_term
FROM grades g
JOIN students s ON g.student_id = s.id
JOIN courses c ON g.course_id = c.id
JOIN colleges cl ON c.college_code = cl.code
```

## 三种角色

### 管理员（Admin）

管理员拥有最高权限，可以：
- 查看所有学生信息，支持按学号/姓名搜索
- 新增/编辑学生，学号按规则自动生成（年+学院+专业+班级序号）
- 查看所有成绩记录，支持跨学院、跨专业搜索
- 录入/编辑/删除任意学生的成绩
- 查看全校仪表盘：学院人数柱状图、班级分布饼图、成绩统计概览

### 教师（Teacher）

教师权限限定在自己所属学院范围内：
- 查看本院学生列表
- 录入/编辑本院学生的成绩
- 搜索本院成绩记录
- 查看本院仪表盘统计

### 学生（Student）

学生只能查看自己的信息：
- 查看个人成绩单（所有学期汇总）
- 查看个人基本信息和学籍信息

## 核心功能

### 学号自动生成

系统按固定编码规则自动生成学号：`年(4位) + 学院代码(2位) + 专业代码(2位) + 班级序号(2位)`，例如 202601010101。新增学生时，管理员选择学院后系统自动获取该学院的专业列表，选择专业后自动计算下一个可用班级序号（每班上限 40 人，超过后自动进下一班）。

### 成绩管理

- 录入成绩：管理员或教师选择学期（年份+学期）和课程，选择学生后录入 0-100 的分数
- 查询成绩：支持模糊搜索 —— 按学号、姓名、课程名、学院名、学期任意组合搜索
- 成绩统计：仪表盘展示各分数段人数分布（0-59 不及格、60-69 及格、70-79 中等、80-89 良好、90-100 优秀）

### 模糊搜索原理

系统采用中文字符级分词策略，使用正则表达式 `re.findall(r'[一-鿿]|[^一-鿿]+', part)` 将搜索词拆分为 token。中文字符逐字拆分，英文/数字保持连续。例如搜索"计算机刘佳"会被拆分为"计、算、机、刘、佳"五个 token，每个 token 分别匹配学号、姓名、课程名、学院名等字段。搜索"2020第一学期"会被拆分为"2020、第、一、学、期"五个 token，配合学期字段的"第X学期"格式进行匹配。这种策略保证了"计算机刘佳"这样中英文混合且词序任意的搜索都能准确命中。

### 前端表单验证

新增/编辑学生时，所有必填字段（姓名、性别、学院、专业、电话）都在提交前进行客户端验证：
- 专业下拉框在选择学院前处于禁用状态，提示"请先选择学院"
- 每个必填字段右侧有红色错误提示区域（field-error），提交时逐项检查
- 学号由系统自动生成，不可手动修改，避免重复和格式错误

## 数据规模

学校数据库预置了完整的教学单位数据：

- **11 个学院**：计算机学院、数学学院、物理学院、化学学院、生命科学学院、经济管理学院、外国语学院、法学院、文学院、艺术学院、体育学院
- **28 个专业**：计算机科学与技术、软件工程、人工智能、数学与应用数学、统计学、物理学、应用物理学、化学、应用化学、生物科学、生物技术、经济学、金融学、工商管理、英语、日语、法学、知识产权、汉语言文学、新闻学、音乐表演、美术学、设计学、体育教育、运动训练等
- **238 门课程**：从高等数学、线性代数等公共基础课到编译原理、机器学习等专业核心课，覆盖所有学院的教学需求
- **1729 名学生**：预置测试数据，分布在 11 个学院 28 个专业中

## 安全设计

- JWT Token 认证：登录成功后返回 token，后续所有 API 请求在 Authorization Header 中携带
- 角色权限控制：每个 API 端点通过装饰器 `@require_role('admin', 'teacher')` 限制访问
- 密码哈希存储：使用 SQLite 的 password_hash 字段存储哈希值，不存明文
- 前端认证检查：页面加载时通过 `checkAuth()` 函数验证 token 有效性和角色

## 项目文件结构

```
Student-Grade-Management-System/
├── app.py              # Flask 应用入口，注册 Blueprint
├── config.py           # 配置文件（数据库路径、密钥）
├── db.py               # 数据库连接 & ATTACH DATABASE 逻辑
├── auth.py             # JWT 认证、角色装饰器、密码哈希
├── schema.sql          # 主数据库建表语句（users, students, grades）
├── school_schema.sql   # 学校数据库建表语句（colleges, majors, courses）
├── seed.py             # 种子数据脚本（1729 名学生 + 238 门课程 + 成绩）
├── api/
│   ├── grade_api.py    # 成绩 CRUD + 模糊搜索
│   ├── student_api.py  # 学生 CRUD
│   ├── course_api.py   # 课程/学院/专业查询
│   └── stats_api.py    # 仪表盘统计数据
├── templates/
│   ├── login.html      # 登录页
│   ├── admin/          # 管理员页面
│   │   ├── dashboard.html
│   │   ├── students.html
│   │   └── grades.html
│   └── teacher/        # 教师页面
│       ├── dashboard.html
│       ├── students.html
│       └── grades.html
└── static/
    ├── css/            # Boomerang UI Kit 样式
    └── js/
        ├── api.js      # 前端 API 封装
        └── auth.js     # 前端认证工具
```
