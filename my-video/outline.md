# Video Outline

> **主题**：`<theme-id>`（Checkpoint Plan 选定后填入）—— 待定
> **总时长**：约 2 分 50 秒（口播 ~2260 字 ÷ ~13 字/秒 B站快节奏）
> **章节数**：6 章 / 30 步

---

## 1. coldopen — 系统初见（4 steps · ~20s）

**信息池**（chapter agent 按需挂角标 / 副标 / pull-quote / mono cue）：
- 技术栈：Flask + SQLite + Bootstrap 4 + jQuery —— 来源 article §系统架构
- 架构：前后端分离，RESTful API，Blueprint 模块化 —— 来源 article §后端技术栈
- 规模：11 学院 / 28 专业 / 238 课程 / 1729 学生 —— 来源 article §数据规模
- 角色：管理员 + 教师 + 学生，JWT 认证 —— 来源 article §三种角色
- 依赖：零外部依赖，一个 Python 环境就能跑 —— 来源 article §安全设计

**开发计划**：

- step 1 (~4s) — 全屏 hero 大字："一个系统，管全校成绩"
- step 2 (~5s) — 大字淡出，副标题切入："不是几十万的教务系统 / 一个人就能搭起来"
- step 3 (~6s) — 三个技术标签依次浮现：Flask / SQLite / Bootstrap 4
- step 4 (~5s) — 底部数字条带横拉出现："11 学院 · 28 专业 · 238 课程 · 1729 学生"

口播节选：
> 你见过一个系统管全校成绩吗？不是那种几十万的教务系统。是一个人就能搭起来的。Flask 加 SQLite，前后端分离，放服务器上就能用。

---

## 2. dual-db — 双数据库架构（5 steps · ~30s）

**信息池**（chapter agent 按需挂角标 / 副标 / pull-quote / mono cue）：
- data.db 表：users、students、grades —— 来源 article §双数据库设计
- school.db 表：colleges、majors、courses —— 来源 article §双数据库设计
- ATTACH DATABASE 语法：`ATTACH DATABASE 'school.db' AS school` —— 来源 article §双数据库设计
- 跨库 JOIN 示例 SQL（article 代码块）—— 来源 article §双数据库设计

**开发计划**：

- step 1 (~6s) — 两个数据库图标/方块并排浮现：data.db（用户数据）| school.db（学校数据）
- step 2 (~5s) — data.db 展开显示三张表：users / students / grades
- step 3 (~5s) — school.db 展开显示三张表：colleges / majors / courses
- step 4 (~6s) — 一条 ATTACH 连线动画，把两个方块桥接起来
- step 5 (~8s) — SQL 代码块逐行高亮：JOIN grades → students → courses → colleges，查询结果行浮现

口播节选：
> 数据库用了两个。用户表、学生表、成绩表放一个库。学院、专业、课程放另一个库。靠一句 ATTACH DATABASE 把 school.db 挂到 data.db 的连接上。然后一条 SQL 就能跨库 JOIN。

---

## 3. roles — 三角色权限（4 steps · ~25s）

**信息池**（chapter agent 按需挂角标 / 副标 / pull-quote / mono cue）：
- 管理员：看全校 / 管全部成绩 / 所有学院数据 —— 来源 article §管理员
- 教师：限定本院范围 / 录入本院成绩 —— 来源 article §教师
- 学生：只看个人成绩单 / 个人信息 —— 来源 article §学生
- JWT：HS256 算法 / Bearer Token / `@require_role` 装饰器 —— 来源 article §安全设计
- 认证流：登录 → token → Authorization Header → 每个请求校验 —— 来源 article §安全设计

**开发计划**：

- step 1 (~6s) — 三个人物图标/卡片并排：管理员 | 教师 | 学生，依次亮起
- step 2 (~8s) — 管理员卡片放大，权限标签逐个出现："全校学生"、"全部成绩"、"仪表盘"
- step 3 (~6s) — 教师和学生卡片轮换点亮，权限范围用光环圈出（全院 vs 个人）
- step 4 (~5s) — JWT token 字符串从左到右流动，经过锁图标，解锁 API 端点列表

口播节选：
> 三种角色。管理员、教师、学生，各有各的权限。管理员看全校，老师看本院，学生只看自己。权限怎么控？JWT。登录拿到 token，后面全靠它。

---

## 4. student-id — 学号自动生成（6 steps · ~35s）

**信息池**（chapter agent 按需挂角标 / 副标 / pull-quote / mono cue）：
- 编码规则：年(4位) + 学院码(2位) + 专业码(2位) + 班级序号(2位) —— 来源 article §学号自动生成
- 示例：2026010101 —— 来源 article §学号自动生成
- 班级上限：40 人/班，满员自动跳下一班 —— 来源 article §学号自动生成
- 联动逻辑：选学院 → API 拉专业列表 → 选专业 → 自动算班号 —— 来源 article §学号自动生成
- 表单验证：5 个必填字段 / 专业下拉初始禁用 / field-error 红色提示 —— 来源 article §前端表单验证

**开发计划**：

- step 1 (~5s) — 学号模板浮现：`____` + `__` + `__` + `__`，标注"年/学院/专业/班级"
- step 2 (~6s) — 模板逐格填入数字：2026 → 01 → 01 → 01，最终显示 2026010101
- step 3 (~7s) — 表单选择流程动画：学院下拉 → 专业 API 加载 → 专业下拉解锁 → 班号自动计算
- step 4 (~6s) — 班级计数器动画：01班 1/40 → 35/40 → 40/40 → 02班 1/40，展示自动进位
- step 5 (~5s) — 表单验证界面：五个必填字段，红色提示逐一亮起又熄灭
- step 6 (~6s) — 完整表单截图，绿色对勾逐个打上："学号自动 / 校验通过 / 提交成功"

口播节选：
> 新增学生的时候，学号不用手填。规则很清晰：四位入学年份，加两位学院代码，加两位专业代码，加两位班级序号。每个班上限 40 人，满了自动进下一班。全程不让你手动输学号，不会重复，不会错。

---

## 5. grade-search — 成绩管理 & 模糊搜索（6 steps · ~35s）

**信息池**（chapter agent 按需挂角标 / 副标 / pull-quote / mono cue）：
- 录入流程：选学期 → 选课程 → 选学生 → 填分数(0-100) —— 来源 article §成绩管理
- 搜索核心：`re.findall(r'[一-鿿]|[^一-鿿]+', part)` 正则分词 —— 来源 article §模糊搜索原理
- 分词规则：中文字逐字拆 / 英文数字保持连续 —— 来源 article §模糊搜索原理
- 匹配字段：学号 / 姓名 / 课程名 / 学院名 / 学期(拼成"第X学期") —— 来源 article §模糊搜索原理
- 搜索示例："计算机刘佳" → 计|算|机|刘|佳 五个 token —— 来源 article §模糊搜索原理

**开发计划**：

- step 1 (~5s) — 成绩录入表单四步流程动画：学期选择器 → 课程选择器 → 学生选择器 → 分数输入框，依次高亮
- step 2 (~6s) — 搜索框特写，用户输入"计算机刘佳"，五个字依次键入
- step 3 (~7s) — 分词动画："计算机刘佳" → 五个方块裂开：计 | 算 | 机 | 刘 | 佳
- step 4 (~6s) — 五个 token 方块各自射出一条线，连接到数据库字段标签：学号、姓名、课程、学院、学期
- step 5 (~5s) — 搜索结果列表浮现，匹配的行高亮，展示命中字段
- step 6 (~6s) — 搜索"2020 第一学期"，数据库字段拼接动画："第" + "1" + "学期" → "第1学期"，匹配成功提示

口播节选：
> 你搜"计算机刘佳"，五个字。系统用正则表达式拆 token。中文字一个一个拆开，英文和数字保持连在一起。然后五个 token 各自去匹配学号、姓名、课程名、学院名。不管你先输学院还是先输名字，都能搜到。

---

## 6. dashboard-wrapup — 仪表盘 & 开箱即用（5 steps · ~25s）

**信息池**（chapter agent 按需挂角标 / 副标 / pull-quote / mono cue）：
- 图表库：ApexCharts.js —— 来源 article §前端技术栈
- 统计维度：学院人数柱状图 / 班级分布饼图 / 成绩分段（0-59/60-69/70-79/80-89/90-100）—— 来源 article §成绩管理
- 11 学院完整名单 —— 来源 article §数据规模
- 28 专业 / 238 课程 —— 来源 article §数据规模
- 启动命令：`python seed.py` → `python app.py` → `localhost:5000` —— 来源 article §项目文件结构
- 部署：零外部依赖 / Nginx 反代 / 无 MySQL/Redis 依赖 —— 来源 article §系统架构

**开发计划**：

- step 1 (~6s) — 仪表盘全景：柱状图生长动画（各学院人数对比），柱体依次从底部弹起
- step 2 (~5s) — 饼图扇形展开动画，各班级占比扇区逐个出现，伴随百分比标签
- step 3 (~5s) — 成绩分段横向条形图：五个分段（不及格→优秀）的横条从左到右生长，数值标注
- step 4 (~6s) — 数据卡片墙：11 个学院名 + 28 个专业名 + 238 课程数 + 1729 学生数，从中心向外扩散排列
- step 5 (~3s) — 终端命令行动画：`$ python seed.py` → `$ python app.py` → `Running on http://127.0.0.1:5000`

口播节选：
> 仪表盘这块也做得不错。柱状图看学院人数，饼图看班级分布，还有成绩分段统计。11 个学院，28 个专业，238 门课，1729 个学生，拿过去就能跑。先 python seed.py 初始化数据库，然后 python app.py 启动服务。

---

## 素材清单

### 1. coldopen
- ⚠️ 系统截图 / 登录页截图（待截取）
- ⚠️ 仪表盘概览截图（待截取）

### 2. dual-db
- ✓ 数据库 schema 已知（schema.sql + school_schema.sql）
- ⚠️ 数据库图标/方块视觉素材（代码绘制，无需外部素材）

### 3. roles
- ⚠️ 角色卡片视觉素材（代码绘制，基于 UI 现有角色设计）

### 4. student-id
- ⚠️ 新增学生表单截图（待截取）
- ✓ 学号生成规则已确认

### 5. grade-search
- ⚠️ 成绩录入 + 搜索结果截图（待截取）
- ✓ 正则分词逻辑已确认

### 6. dashboard-wrapup
- ⚠️ 仪表盘图表截图（待截取，含柱状图+饼图+分段统计）

---
