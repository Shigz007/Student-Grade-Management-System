$ErrorActionPreference = "Stop"

$docPath = "c:\Users\Shigz007\Desktop\Student-Grade-Management-System\图书馆座位管理系统-预约模块-需求说明书-欧彤-v1.0.doc"
$newDocPath = "c:\Users\Shigz007\Desktop\Student-Grade-Management-System\学生成绩管理系统-成绩管理模块-需求说明书-欧彤-v1.0.docx"

Write-Host "Starting Word COM..."
$word = New-Object -ComObject Word.Application
$word.Visible = $false

# Open the existing document
$doc = $word.Documents.Open($docPath)

# Clear all content
$doc.Content.Delete()

$range = $doc.Content
$selection = $word.Selection

# ============ HELPER FUNCTIONS ============

function AddParagraph($text, $style, $bold, $size, $alignment, $spaceAfter, $spaceBefore) {
    $selection.Style = $style
    if ($bold) { $selection.Font.Bold = $bold }
    if ($size) { $selection.Font.Size = $size }
    if ($alignment) { $selection.ParagraphFormat.Alignment = $alignment }
    if ($spaceAfter -ne $null) { $selection.ParagraphFormat.SpaceAfter = $spaceAfter }
    if ($spaceBefore -ne $null) { $selection.ParagraphFormat.SpaceBefore = $spaceBefore }
    $selection.TypeText($text)
    $selection.TypeParagraph()
}

function AddTable($rows, $cols, $data, $colWidths) {
    $table = $selection.Tables.Add($selection.Range, $rows, $cols, 1, 0)
    $table.Borders.Enable = $true
    for ($r = 0; $r -lt $rows; $r++) {
        for ($c = 0; $c -lt $cols; $c++) {
            $cell = $table.Cell($r + 1, $c + 1)
            $cell.Range.Text = $data[$r][$c]
            $cell.Range.Font.Size = 10.5
            if ($r -eq 0) {
                $cell.Range.Font.Bold = $true
                $cell.Shading.BackgroundPatternColor = 15724527  # light gray
            }
        }
    }
    if ($colWidths) {
        for ($c = 0; $c -lt $cols; $c++) {
            $table.Columns.Item($c + 1).PreferredWidth = $colWidths[$c]
        }
    }
    $selection.EndOf(6)  # wdStory
    $selection.TypeParagraph()
}

# ============ COVER PAGE ============

# Center alignment
$selection.ParagraphFormat.Alignment = 1  # wdAlignParagraphCenter

# School header
AddParagraph "计算机科学与技术（国际人才培养班）(专升本）" "Normal" $false 14 1 0 0
AddParagraph "课程设计" "Normal" $true 18 1 12 12

# Blank line
$selection.TypeParagraph()
$selection.TypeParagraph()

# Title
AddParagraph "题    目：" "Normal" $true 14 1 6 6
AddParagraph "基于Flask和Vue3的学生成绩管理系统" "Normal" $true 16 1 12 6

$selection.TypeParagraph()
$selection.TypeParagraph()

# Team members table
$selection.TypeParagraph()
$teamData = @(
    @("姓名", "负责模块"),
    @("欧彤", "成绩管理模块"),
    @("黄嘉文", "意见反馈管理"),
    @("程塬歆", "学生管理、课程管理"),
    @("尹姗姗", "常见问题管理")
)
AddTable 5 2 $teamData @(200, 260)

$selection.TypeParagraph()

# Course info
AddParagraph "课程名称：" "Normal" $true 12 0 6 0
AddParagraph "计算机专业综合实践Ⅰ" "Normal" $false 12 0 6 0
$selection.TypeParagraph()
AddParagraph "专    业：" "Normal" $true 12 0 6 0
AddParagraph "计算机科学与技术" "Normal" $false 12 0 6 0
$selection.TypeParagraph()
AddParagraph "班    级：" "Normal" $true 12 0 6 0
AddParagraph "23本计算机科学与技术（国际班）（专升本）班" "Normal" $false 12 0 6 0
$selection.TypeParagraph()
AddParagraph "指导老师：" "Normal" $true 12 0 6 0
AddParagraph "梁子华" "Normal" $false 12 0 6 0
$selection.TypeParagraph()
AddParagraph "完成时间：" "Normal" $true 12 0 6 0
AddParagraph "2026年05月28日" "Normal" $false 12 0 6 0

# ============ PAGE BREAK for TOC ============
$selection.InsertBreak(7)  # wdPageBreak

# ============ TABLE OF CONTENTS ============
$selection.ParagraphFormat.Alignment = 1
AddParagraph "目    录" "Heading 1" $true 16 1 12 12
$selection.TypeParagraph()

$tocItems = @(
    "第1章  引  言",
    "1.1  项目背景",
    "1.2  定义",
    "1.3  建设目标",
    "第2章  需求建模",
    "2.1  成绩管理业务需求描述",
    "2.2  成绩管理功能需求分析",
    "2.3  对象模型分析",
    "2.4  非功能需求分析"
)

$selection.ParagraphFormat.Alignment = 0  # left align
foreach ($item in $tocItems) {
    AddParagraph $item "Normal" $false 12 0 4 2
}

# ============ PAGE BREAK ============
$selection.InsertBreak(7)

# ============ CHAPTER 1: INTRODUCTION ============
$selection.ParagraphFormat.Alignment = 0
AddParagraph "第1章  引  言" "Heading 1" $true 16 0 12 12

# 1.1
AddParagraph "1.1  项目背景" "Heading 2" $true 14 0 8 8

$bg1 = "在当今教育信息化时代，学生成绩管理是学校教学管理的核心环节之一。传统的成绩管理方式存在数据分散、查询不便、统计困难等问题，给教师和管理人员带来了较大工作负担。为了更好地满足教学管理需求，提升成绩管理的效率和准确性，我们开发了学生成绩管理系统。"
$selection.TypeText($bg1)
$selection.TypeParagraph()
$selection.TypeParagraph()

$bg2 = "学生成绩管理系统利用Flask框架和Vue3前端技术，结合ECharts图表进行统计分析，使用SQLite数据库实现数据持久化存储，帮助教师和管理人员高效地管理学生信息、录入和查询成绩、进行成绩统计分析，为学生提供便捷的成绩查询服务。采用前后端分离架构，前端使用Vue3 + TypeScript + Vite构建，后端使用Python Flask框架提供RESTful API，通过JWT Token实现身份认证和权限控制。"
$selection.TypeText($bg2)
$selection.TypeParagraph()
$selection.TypeParagraph()

$bg3 = "随着互联网和移动设备的普及，师生对于教学服务的需求不再局限于传统方式，而是更注重方便、快捷、个性化的服务体验。学生成绩管理系统提供了更便捷的服务，用户可以进行的操作包括查询成绩、查看成绩统计、管理学生信息、录入和修改成绩、管理课程信息等，管理员可以管理学生信息、管理教师账号、管理课程数据、进行成绩统计分析等。这为学校的成绩管理提供了更加高效和便捷的方式。"
$selection.TypeText($bg3)
$selection.TypeParagraph()

# 1.2
AddParagraph "1.2  定义" "Heading 2" $true 14 0 8 8

# 1.2.1 SGMS
AddParagraph "1.2.1  SGMS" "Heading 3" $true 12 0 6 6
$sgms = "SGMS（Student Grade Management System，学生成绩管理系统）是一个基于Web的成绩管理平台，通过对学生成绩数据、课程信息、学生信息等进行统一管理和深入分析，为教师、学生和管理员提供数据支持，以便更好地管理和优化教学资源，满足用户的需求。系统采用前后端分离架构，前端使用Vue3 + TypeScript + Vite构建SPA应用，后端使用Python Flask框架提供RESTful API接口。"
$selection.TypeText($sgms)
$selection.TypeParagraph()

# 1.2.2 Flask
AddParagraph "1.2.2  Flask" "Heading 3" $true 12 0 6 6
$flaskIntro = "Flask是一个轻量级的Python Web框架，基于Werkzeug工具箱和Jinja2模板引擎。Flask具有以下主要特点和优势："
$selection.TypeText($flaskIntro)
$selection.TypeParagraph()

$flaskFeatures = @(
    "轻量灵活：Flask核心简单但扩展性强，开发者可以根据需要灵活选择扩展组件。",
    "易于上手：Flask的设计简洁，学习曲线平缓，适合快速开发Web应用。",
    "RESTful支持：Flask天然支持RESTful API设计，通过Blueprint实现模块化路由管理，本系统中的auth、student、grade、course等API均基于Blueprint构建。",
    "Jinja2模板：内置强大的Jinja2模板引擎，支持模板继承和宏定义，便于构建动态页面和后台管理界面。",
    "丰富的扩展生态：Flask拥有丰富的扩展库，如Flask-CORS处理跨域请求，便于前后端分离开发。",
    "开发服务器：内置开发服务器，支持调试模式和热重载，提高开发效率。"
)
foreach ($f in $flaskFeatures) {
    $selection.TypeText($f)
    $selection.TypeParagraph()
}

# 1.2.3 Vue3
AddParagraph "1.2.3  Vue3" "Heading 3" $true 12 0 6 6
$vue3 = "Vue 3是Vue.js框架的最新版本，于2020年9月正式发布。它是一种流行的JavaScript框架，用于构建用户界面。Vue 3在Vue 2的基础上进行了重大改进和增强，提供了更好的性能、更好的开发体验和更多的功能。Vue 3引入了一种新的组合式API（Composition API），用于将组件的逻辑按照功能进行组织，使代码更加清晰易懂和可复用。本系统前端采用Vue3 + TypeScript + Vite构建，实现响应式数据绑定和组件化开发。相对于Vue 2中的Options API，Composition API更清晰地展示了复用功能代码的来源，使代码更加清晰易懂。"
$selection.TypeText($vue3)
$selection.TypeParagraph()

# 1.2.4 SQLite
AddParagraph "1.2.4  SQLite" "Heading 3" $true 12 0 6 6
$sqlite = "SQLite是一个轻量级的嵌入式关系型数据库，它不需要独立的服务器进程，将整个数据库存储在一个单一的文件中。SQLite具有零配置、轻量高效、跨平台和ACID兼容等特点。本系统采用SQLite作为数据库，分为主数据库（data.db）存储用户、学生和成绩数据，以及学校数据库（school.db）存储学院、专业和课程数据。两个数据库通过ATTACH DATABASE机制关联查询，实现了数据的逻辑分离。相较于Redis等内存缓存方案，SQLite更适合本系统的数据规模和部署场景，无需额外的服务器进程，降低了运维复杂度。"
$selection.TypeText($sqlite)
$selection.TypeParagraph()

# 1.2.5 ECharts
AddParagraph "1.2.5  ECharts" "Heading 3" $true 12 0 6 6
$echarts = "ECharts是一个基于JavaScript的开源可视化图表库，由百度开发和维护。它提供了丰富的图表类型和交互功能，包括柱状图、折线图、饼图、散点图等。在本系统中，ECharts用于展示成绩统计数据的可视化分析，如成绩分布图、及格率统计等，帮助教师和管理员直观地了解学生的学习情况和成绩趋势。"
$selection.TypeText($echarts)
$selection.TypeParagraph()

# 1.3
AddParagraph "1.3  建设目标" "Heading 2" $true 14 0 8 8

$goalIntro = "学生成绩管理系统以为学生提供便捷的成绩查询服务，为教师提供高效的成绩管理工具，为管理员提供全面的系统管理功能进行建设，以下是学生成绩管理系统的建设目标："
$selection.TypeText($goalIntro)
$selection.TypeParagraph()
$selection.TypeParagraph()

$goals = @(
    "①提高成绩管理效率：通过系统化的成绩管理，实现成绩的快速录入、修改、查询和删除，减少人工操作和纸质记录，提高教学管理的工作效率。",
    "②提升数据准确性：通过数据校验机制（如成绩范围0-100验证、学号唯一性检查等），确保成绩数据的准确性和完整性，避免人为录入错误。",
    "③提高用户体验：系统提供友好的用户界面和便捷的操作流程，学生可以快速查询个人成绩和统计信息，教师可以高效管理班级和成绩，管理员可以全面掌控系统数据。",
    "④数据分析和决策支持：系统收集和分析成绩数据，提供平均分、最高分、最低分、及格率等统计指标，通过ECharts图表直观展示成绩分布趋势，为教学决策提供数据支持。",
    "⑤加强权限管理：系统实现了基于JWT的三级角色权限控制，分为管理员（admin）、教师（teacher）和学生（student），通过装饰器@login_required、@teacher_or_admin、@admin_required严格控制API访问权限，确保数据安全。",
    "⑥支持移动端访问：随着移动设备的普及，系统提供友好的响应式界面和Bootstrap UI组件，方便师生随时随地进行成绩的查询和管理。",
    "⑦系统轻量化部署：采用SQLite嵌入式数据库和Flask轻量框架，系统无需安装额外的数据库服务器，可实现快速部署和低运维成本运行。"
)
foreach ($g in $goals) {
    $selection.TypeText($g)
    $selection.TypeParagraph()
    $selection.TypeParagraph()
}

# ============ PAGE BREAK ============
$selection.InsertBreak(7)

# ============ CHAPTER 2: REQUIREMENTS MODELING ============
AddParagraph "第2章  需求建模" "Heading 1" $true 16 0 12 12

# 2.1
AddParagraph "2.1  成绩管理业务需求描述" "Heading 2" $true 14 0 8 8

$biz1 = "成绩管理模块主要由学生端、教师端和管理员端构成。学生端主要的业务包含查看个人成绩列表（支持按学年学期和课程筛选）、查看个人成绩统计分析（平均分、最高分、最低分、及格率）以及修改个人登录密码。学生在登录后进入学生后台界面，可以查看自己所有课程的成绩记录，系统会实时计算并展示成绩统计信息。"
$selection.TypeText($biz1)
$selection.TypeParagraph()
$selection.TypeParagraph()

$biz2 = "教师端包括查看所管辖学生的成绩列表、为学生录入成绩（需选择学生、课程、填写分数和学年学期信息）、修改已录入的成绩、删除错误的成绩记录、查看成绩统计数据。教师登录后进入教师后台界面，可以进行成绩的增删改查操作，支持按学号、姓名、课程名称、学年学期等多个条件进行组合搜索。"
$selection.TypeText($biz2)
$selection.TypeParagraph()
$selection.TypeParagraph()

$biz3 = "管理员端包括所有教师端的功能，此外还可以管理学生信息（增加、修改、删除学生）、管理课程和学院专业数据、查看所有成绩记录和全局统计。管理员登录后进入管理员后台界面，拥有系统的全部操作权限。系统在添加学生时会自动按照年级+学院+专业+班级+序号的规则生成学号，并自动创建学生登录账号（默认密码Ad112233）。"
$selection.TypeText($biz3)
$selection.TypeParagraph()

# 2.2
AddParagraph "2.2  成绩管理功能需求分析" "Heading 2" $true 14 0 8 8

AddParagraph "2.2.1  功能概述" "Heading 3" $true 12 0 6 6

$features = @{
    "成绩录入" = "教师和管理员能够为学生录入成绩，填写学生信息、课程信息、分数（0-100分）、学年和学期信息。系统会对输入数据进行校验，确保成绩在有效范围内，学号和课程信息有效。"
    "成绩查询" = "用户能够按多种条件查询成绩，包括学生ID、课程ID、学年、学期以及多关键词模糊搜索（支持学号、姓名、课程名等）。学生只能查看自己的成绩，教师和管理员可查看所有学生成绩。查询结果按记录ID倒序排列。"
    "成绩修改" = "教师和管理员能够修改已录入的成绩记录，系统保留修改前的数据校验机制（成绩范围验证、记录存在性检查等），确保数据更新的安全性和准确性。"
    "成绩删除" = "教师和管理员能够删除错误的成绩记录，删除前系统会验证记录是否存在。删除学生时，系统会自动级联删除该学生关联的所有成绩记录。"
    "成绩统计" = "系统提供成绩统计分析接口，计算平均分、最高分、最低分、及格率（60分及以上为及格）和成绩总数。学生仅可查看个人统计，教师和管理员可查看全局或指定学生的统计。前端通过ECharts图表可视化展示统计数据。"
    "学年学期管理" = "系统支持按学年和学期（如2025-2026学年第1学期）对成绩进行分类管理，查询成绩时可获取系统中已存在的所有学年列表，便于筛选。"
    "学生信息管理（关联功能）" = "管理员和教师可添加、修改、删除学生信息。添加学生时系统自动计算并生成学号（格式：年级后2位+学院代码+专业代码+班级序号+学生序号），支持班级人数上限控制（每班40人），并自动创建对应的登录账号。"
    "课程与学院数据（关联功能）" = "系统维护学院（colleges）、专业（majors）和课程（courses）的基础数据，支持按学院和专业筛选课程列表，为成绩录入和查询提供基础数据支撑。"
}

foreach ($key in $features.Keys) {
    $selection.Font.Bold = $true
    $selection.TypeText("$key：")
    $selection.Font.Bold = $false
    $selection.TypeText($features[$key])
    $selection.TypeParagraph()
    $selection.TypeParagraph()
}

# 2.2.2 Use cases
AddParagraph "2.2.2  用例分析" "Heading 3" $true 12 0 6 6

# Use Case Table Helper
function AddUseCaseTable($caseData) {
    $rows = $caseData.Count
    $data = @()
    foreach ($pair in $caseData.GetEnumerator()) {
        $data += @($pair.Key, $pair.Value)
    }

    $table = $selection.Tables.Add($selection.Range, $rows, 2, 1, 0)
    $table.Borders.Enable = $true
    $table.Columns.Item(1).PreferredWidth = 80
    $table.Columns.Item(2).PreferredWidth = 400

    $i = 0
    foreach ($pair in $caseData.GetEnumerator()) {
        $r = $i + 1
        $cellKey = $table.Cell($r, 1)
        $cellKey.Range.Text = $pair.Key
        $cellKey.Range.Font.Bold = $true
        $cellKey.Range.Font.Size = 10.5
        $cellKey.Shading.BackgroundPatternColor = 15724527

        $cellVal = $table.Cell($r, 2)
        $cellVal.Range.Text = $pair.Value
        $cellVal.Range.Font.Size = 10.5
        $i++
    }

    $selection.EndOf(6)
    $selection.TypeParagraph()
    $selection.TypeParagraph()
}

# --- Use Case 1: 成绩录入 ---
$selection.Font.Bold = $true
$selection.TypeText("表2-1 成绩录入用例描述")
$selection.Font.Bold = $false
$selection.TypeParagraph()
$selection.TypeParagraph()

AddUseCaseTable ([ordered]@{
    "ID" = "SGMS0001"
    "用例名称" = "成绩录入"
    "父用例ID" = "-"
    "主要执行者" = "教师、管理员"
    "前置条件" = "1. 登录系统`n2. 具有教师或管理员权限"
    "事件流" = "1. 进入成绩管理界面`n2. 选择学生和课程`n3. 填写分数（0-100分）和学期信息`n4. 提交保存"
    "可选事件流" = "-"
    "异常事件流" = "1. 成绩不在0-100范围时，弹出错误提示`"成绩必须在0-100之间`"`n2. 未选择学生或课程时，弹出提示`"学生、课程和成绩不能为空`""
    "后置条件" = "成绩记录添加到成绩表（grades表），返回录入成功的消息"
})

# --- Use Case 2: 成绩查询 ---
$selection.Font.Bold = $true
$selection.TypeText("表2-2 成绩查询用例描述")
$selection.Font.Bold = $false
$selection.TypeParagraph()
$selection.TypeParagraph()

AddUseCaseTable ([ordered]@{
    "ID" = "SGMS0002"
    "用例名称" = "成绩查询"
    "父用例ID" = "-"
    "主要执行者" = "学生、教师、管理员"
    "前置条件" = "登录系统"
    "事件流" = "1. 进入成绩管理界面`n2. 可按学生ID、课程ID、学年、学期等条件筛选`n3. 支持多关键词模糊搜索（匹配学号、姓名、课程名、学院名、学期信息）"
    "可选事件流" = "学生角色自动识别身份，仅返回本人的成绩数据"
    "异常事件流" = "学生尝试查询他人成绩时，系统仅返回本人数据（权限控制）"
    "后置条件" = "展示成绩列表，按记录ID倒序排列，包含学生姓名、学号、课程名称、分数、学期等信息"
})

# --- Use Case 3: 成绩修改 ---
$selection.Font.Bold = $true
$selection.TypeText("表2-3 成绩修改用例描述")
$selection.Font.Bold = $false
$selection.TypeParagraph()
$selection.TypeParagraph()

AddUseCaseTable ([ordered]@{
    "ID" = "SGMS0003"
    "用例名称" = "成绩修改"
    "父用例ID" = "-"
    "主要执行者" = "教师、管理员"
    "前置条件" = "1. 登录系统`n2. 目标成绩记录存在"
    "事件流" = "1. 选中需要修改的成绩记录`n2. 修改成绩信息（学生、课程、分数、学期等）`n3. 提交更新请求"
    "可选事件流" = "可部分修改，仅更新传入的字段"
    "异常事件流" = "1. 成绩记录不存在时，返回404错误`"成绩记录不存在`"`n2. 修改后的成绩不在0-100范围时，返回错误提示`"成绩必须在0-100之间`""
    "后置条件" = "成绩记录更新，返回更新成功的消息"
})

# --- Use Case 4: 成绩删除 ---
$selection.Font.Bold = $true
$selection.TypeText("表2-4 成绩删除用例描述")
$selection.Font.Bold = $false
$selection.TypeParagraph()
$selection.TypeParagraph()

AddUseCaseTable ([ordered]@{
    "ID" = "SGMS0004"
    "用例名称" = "成绩删除"
    "父用例ID" = "-"
    "主要执行者" = "教师、管理员"
    "前置条件" = "1. 登录系统`n2. 目标成绩记录存在"
    "事件流" = "1. 选中需要删除的成绩记录`n2. 确认删除操作`n3. 系统删除记录"
    "可选事件流" = "删除学生时，系统自动级联删除该学生的所有成绩记录"
    "异常事件流" = "成绩记录不存在时，返回404错误`"成绩记录不存在`""
    "后置条件" = "成绩记录从成绩表（grades表）中永久移除，返回删除成功的消息"
})

# --- Use Case 5: 成绩统计 ---
$selection.Font.Bold = $true
$selection.TypeText("表2-5 成绩统计用例描述")
$selection.Font.Bold = $false
$selection.TypeParagraph()
$selection.TypeParagraph()

AddUseCaseTable ([ordered]@{
    "ID" = "SGMS0005"
    "用例名称" = "成绩统计"
    "父用例ID" = "-"
    "主要执行者" = "学生、教师、管理员"
    "前置条件" = "登录系统"
    "事件流" = "1. 进入成绩统计界面`n2. 系统自动计算并展示统计数据：平均分、最高分、最低分、及格率、成绩总数`n3. 前端通过ECharts图表直观展示成绩分布"
    "可选事件流" = "学生查看个人统计；教师和管理员可查看全局统计或指定学生的统计"
    "异常事件流" = "无成绩数据时，各项统计指标均显示为0"
    "后置条件" = "展示统计结果（JSON格式返回avg/max/min/pass_rate/count字段）"
})

# 2.3 Object Model
AddParagraph "2.3  对象模型分析" "Heading 2" $true 14 0 8 8

$objIntro = "系统核心实体及其属性定义如下："
$selection.TypeText($objIntro)
$selection.TypeParagraph()
$selection.TypeParagraph()

# Entity descriptions
$entities = @{
    "用户（User）" = "id（主键）、username（用户名，唯一）、password_hash（密码哈希值）、role（角色：admin/teacher/student）、created_at（创建时间）"
    "学生（Student）" = "id（主键）、student_no（学号，唯一）、name（姓名）、gender（性别）、enrollment_year（入学年份）、college_code（学院代码）、major_code（专业代码）、class_name（班级名称）、phone（电话）、email（邮箱）、created_at（创建时间）"
    "成绩（Grade）" = "id（主键）、student_id（外键→Student）、course_id（外键→Course）、score（分数，0-100）、semester_year（学年）、semester_term（学期）、created_at（创建时间）"
    "课程（Course）" = "id（主键）、code（课程代码，唯一）、name（课程名称）、college_code（外键→College）、major_code（专业代码）"
    "学院（College）" = "code（主键）、name（学院名称，唯一）"
    "专业（Major）" = "id（主键）、code（专业代码）、name（专业名称）、college_code（外键→College）"
}

foreach ($key in $entities.Keys) {
    $selection.Font.Bold = $true
    $selection.TypeText("$key：")
    $selection.Font.Bold = $false
    $selection.TypeText($entities[$key])
    $selection.TypeParagraph()
}

$selection.TypeParagraph()

$relIntro = "实体间关系说明："
$selection.Font.Bold = $true
$selection.TypeText($relIntro)
$selection.Font.Bold = $false
$selection.TypeParagraph()

$relations = @(
    "一个学生（Student）可以有多条成绩记录（Grade），形成一对多关系，通过student_id外键关联。",
    "一门课程（Course）可以关联多条成绩记录（Grade），形成一对多关系，通过course_id外键关联。",
    "一个学院（College）包含多个专业（Major），形成一对多关系，通过college_code外键关联。",
    "一个学院（College）包含多门课程（Course），形成一对多关系，通过college_code外键关联。",
    "用户（User）与学生（Student）通过username与name字段隐式关联，学生登录时由系统自动匹配身份。"
)
foreach ($r in $relations) {
    $selection.TypeText("· $r")
    $selection.TypeParagraph()
}

$selection.TypeParagraph()

# Database architecture note
$dbArch = "数据库架构说明：系统采用双数据库设计，将核心业务数据与基础数据分离。data.db存储运行时数据（用户、学生、成绩），school.db存储相对静态的学校基础数据（学院、专业、课程）。通过SQLite的ATTACH DATABASE机制，成绩查询时可跨数据库JOIN查询，如将成绩表关联学生表（data.db）和课程表、学院表（school.db），实现一次查询获取完整信息。"
$selection.TypeText($dbArch)
$selection.TypeParagraph()

# 2.4
AddParagraph "2.4  非功能需求分析" "Heading 2" $true 14 0 8 8

# Non-functional requirements - I'll write these as structured text with headings
$nfrSections = @{
    "1. 性能需求" = @{
        "1.1 响应速度" = "目标：应保证系统对用户请求的快速响应，特别是在成绩查询和统计计算的高峰期。`n指标：95%的请求响应时间应在2秒以内。"
        "1.2 结果精度" = "目标：应保证成绩统计计算结果的准确性和数据一致性。`n指标：成绩统计计算结果的准确率应在99%以上。"
        "1.3 运行时资源消耗" = "目标：应保证系统在运行时消耗的资源合理，不超过服务器性能的合理范围。`n指标：系统运行时内存占用不超过2GB，CPU占用不超过80%。"
    }
    "2. 可靠性需求" = @{
        "2.1 失效频率" = "目标：应保证系统的失效频率较低，确保用户正常使用。`n指标：平均无故障时间（MTBF）不低于1000小时。"
        "2.2 失效严重程度" = "目标：应保证系统失效时对用户的影响较小。`n指标：平均恢复时间（MTTR）不超过30分钟。"
        "2.3 故障可预测性" = "目标：应提前检测潜在故障，以减少系统失效的意外情况。`n指标：实施主动巡检，提前预警系统可能的故障。"
    }
    "3. 易用性需求" = @{
        "3.1 界面易用性" = "目标：界面设计应简洁直观，用户容易上手，不同角色（学生/教师/管理员）的操作路径清晰。`n指标：用户满意度调查结果在80%以上。"
        "3.2 美观性" = "目标：界面设计应美观，采用Bootstrap UI框架，符合用户审美。`n指标：界面设计专业评估得分不低于4分（满分5分）。"
        "3.3 文档和培训资料" = "目标：提供详细的用户文档和培训资料，帮助用户了解系统使用。`n指标：用户手册完整覆盖系统功能，提供在线培训视频。"
    }
    "4. 安全性需求" = @{
        "4.1 身份认证" = "目标：用户身份应得到有效认证，确保系统安全性。`n指标：采用JWT Token机制和密码哈希加密（Werkzeug generate_password_hash）进行安全认证。"
        "4.2 授权控制" = "目标：确保用户只能访问其权限范围内的功能和数据。`n指标：通过三级装饰器（@login_required基础认证、@teacher_or_admin教师及以上、@admin_required仅管理员）严格控制API权限。学生只能查看本人成绩，教师和管理员按权限访问。"
        "4.3 私密性" = "目标：用户的个人信息和成绩数据应得到保护，不被未授权人员访问。`n指标：密码以哈希形式存储，成绩数据按角色隔离。"
    }
    "5. 运行环境约束" = @{
        "目标" = "系统应能在常见的浏览器和操作系统下运行。`n约束：支持主流浏览器（Chrome、Firefox、Safari、Edge）和操作系统（Windows、macOS、Linux）。Python 3.x运行环境，无需额外数据库服务器安装。"
    }
    "6. 外部接口" = @{
        "目标" = "系统应能与学校其他管理系统进行良好的集成。`n接口：提供标准RESTful API接口（JSON格式），支持与学生信息系统的数据对接。API设计遵循REST规范，使用标准HTTP方法（GET/POST/PUT/DELETE）。"
    }
}

foreach ($section in $nfrSections.Keys) {
    AddParagraph $section "Heading 3" $true 12 0 6 6

    $subSections = $nfrSections[$section]
    foreach ($sub in $subSections.Keys) {
        if ($sub -ne "目标") {
            AddParagraph $sub "Normal" $true 10.5 0 3 2
        }
        $selection.Font.Bold = $false
        $selection.TypeText($subSections[$sub] -replace '`n', "`r`n")
        $selection.TypeParagraph()
        $selection.TypeParagraph()
    }
}

# ============ SAVE ============
Write-Host "Saving document to: $newDocPath"
$doc.SaveAs2($newDocPath, 16)  # 16 = wdFormatDocumentDefault (.docx)
$doc.Close()
$word.Quit()

Write-Host "Document rebuilt successfully!"
Write-Host "New file: $newDocPath"
Write-Host "Original file preserved at: $docPath"

# Release COM objects
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($selection) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($doc) | Out-Null
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
[System.GC]::Collect()
[System.GC]::WaitForPendingFinalizers()

