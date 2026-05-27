from flask import Blueprint, request, jsonify, g
import re
from auth import login_required, teacher_or_admin, admin_required
from db import query, execute

grade_bp = Blueprint('grade', __name__)


@grade_bp.route('/api/grades', methods=['GET'])
@login_required
def get_grades():
    student_id = request.args.get('student_id', '').strip()
    semester_year = request.args.get('semester_year', '').strip()
    semester_term = request.args.get('semester_term', '').strip()
    course_id = request.args.get('course_id', '').strip()
    college_code = request.args.get('college_code', '').strip()
    major_code = request.args.get('major_code', '').strip()
    search = request.args.get('search', '').strip()

    where = []
    args = []

    if g.user['role'] == 'student':
        user = query("SELECT * FROM users WHERE id = ?", (g.user['user_id'],), one=True)
        student = query("SELECT * FROM students WHERE name = ?", (user['username'],), one=True)
        if student:
            where.append("g.student_id = ?")
            args.append(student['id'])
        else:
            return jsonify([])
    elif g.user['role'] == 'teacher':
        tcs = query("SELECT college_code, major_code, class_name FROM teacher_classes WHERE user_id = ?",
                    (g.user['user_id'],))
        if not tcs:
            return jsonify([])
        tconds = []
        for tc in tcs:
            tconds.append("(s.college_code = ? AND s.major_code = ? AND SUBSTR(s.student_no, 7, 2) = ?)")
            args.extend([tc['college_code'], tc['major_code'], tc['class_name']])
        where.append("(" + " OR ".join(tconds) + ")")
    elif student_id:
        where.append("g.student_id = ?")
        args.append(int(student_id))

    if search:
        for part in search.split():
            for token in re.findall(r'[一-鿿]|[^一-鿿]+', part):
                where.append("(s.name || s.student_no || c.name || cl.name || g.semester_year || '第' || g.semester_term || '学期') LIKE ?")
                args.append('%' + token + '%')

    if semester_year:
        where.append("g.semester_year = ?")
        args.append(semester_year)
    if semester_term:
        where.append("g.semester_term = ?")
        args.append(semester_term)
    if course_id:
        where.append("g.course_id = ?")
        args.append(int(course_id))
    if college_code:
        where.append("c.college_code = ?")
        args.append(college_code)
    if major_code:
        where.append("c.major_code = ?")
        args.append(major_code)

    sql = """
        SELECT g.*, s.name as student_name, s.student_no,
               c.name as course_name, c.code as course_code,
               cl.name as college_name, c.college_code,
               m.name as major_name
        FROM grades g
        JOIN students s ON g.student_id = s.id
        JOIN courses c ON g.course_id = c.id
        JOIN colleges cl ON c.college_code = cl.code
        JOIN majors m ON c.college_code = m.college_code AND c.major_code = m.code
    """
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY g.id DESC"

    return jsonify(query(sql, args))


@grade_bp.route('/api/grades', methods=['POST'])
@teacher_or_admin
def add_grade():
    data = request.get_json()
    student_id = data.get('student_id')
    course_id = data.get('course_id')
    score = data.get('score')

    if not student_id or not course_id or score is None:
        return jsonify({'error': '学生、课程和成绩不能为空'}), 400
    if not (0 <= float(score) <= 100):
        return jsonify({'error': '成绩必须在0-100之间'}), 400

    if g.user['role'] == 'teacher':
        student = query("SELECT * FROM students WHERE id = ?", (int(student_id),), one=True)
        if not student:
            return jsonify({'error': '学生不存在'}), 404
        tcs = query("SELECT * FROM teacher_classes WHERE user_id = ? AND college_code = ? AND major_code = ? AND class_name = ?",
                    (g.user['user_id'], student['college_code'], student['major_code'],
                     student['student_no'][6:8] if student['student_no'] and len(student['student_no']) >= 8 else ''))
        if not tcs:
            return jsonify({'error': '该学生不在您分配的班级范围内'}), 403

    gid = execute(
        "INSERT INTO grades (student_id, course_id, score, semester_year, semester_term) VALUES (?,?,?,?,?)",
        (int(student_id), int(course_id), float(score),
         data.get('semester_year', ''), data.get('semester_term', ''))
    )
    return jsonify({'id': gid, 'message': '录入成功'}), 201


@grade_bp.route('/api/grades/<int:gid>', methods=['PUT'])
@teacher_or_admin
def update_grade(gid):
    data = request.get_json()
    grade = query("SELECT * FROM grades WHERE id = ?", (gid,), one=True)
    if not grade:
        return jsonify({'error': '成绩记录不存在'}), 404

    score = data.get('score', grade['score'])
    if not (0 <= float(score) <= 100):
        return jsonify({'error': '成绩必须在0-100之间'}), 400

    execute(
        "UPDATE grades SET student_id=?, course_id=?, score=?, semester_year=?, semester_term=? WHERE id=?",
        (data.get('student_id', grade['student_id']),
         data.get('course_id', grade['course_id']),
         float(score),
         data.get('semester_year', grade['semester_year']),
         data.get('semester_term', grade['semester_term']),
         gid)
    )
    return jsonify({'message': '更新成功'})


@grade_bp.route('/api/grades/<int:gid>', methods=['DELETE'])
@admin_required
def delete_grade(gid):
    grade = query("SELECT * FROM grades WHERE id = ?", (gid,), one=True)
    if not grade:
        return jsonify({'error': '成绩记录不存在'}), 404
    execute("DELETE FROM grades WHERE id = ?", (gid,))
    return jsonify({'message': '删除成功'})


@grade_bp.route('/api/grades/years', methods=['GET'])
@login_required
def get_years():
    if g.user['role'] == 'teacher':
        tcs = query("SELECT college_code, major_code, class_name FROM teacher_classes WHERE user_id = ?",
                    (g.user['user_id'],))
        if not tcs:
            return jsonify([])
        conds = []
        args = []
        for tc in tcs:
            conds.append("(s.college_code = ? AND s.major_code = ? AND SUBSTR(s.student_no, 7, 2) = ?)")
            args.extend([tc['college_code'], tc['major_code'], tc['class_name']])
        rows = query(
            "SELECT DISTINCT g.semester_year FROM grades g JOIN students s ON g.student_id = s.id WHERE g.semester_year != '' AND (" + " OR ".join(conds) + ") ORDER BY g.semester_year",
            args
        )
    else:
        rows = query("SELECT DISTINCT semester_year FROM grades WHERE semester_year != '' ORDER BY semester_year")
    return jsonify([r['semester_year'] for r in rows])


@grade_bp.route('/api/grades/stats', methods=['GET'])
@login_required
def get_stats():
    if g.user['role'] == 'student':
        user = query("SELECT * FROM users WHERE id = ?", (g.user['user_id'],), one=True)
        student = query("SELECT * FROM students WHERE name = ?", (user['username'],), one=True)
        student_id = student['id'] if student else None
    else:
        student_id = request.args.get('student_id', '').strip()
        student_id = int(student_id) if student_id else None

    if student_id:
        grades = query("SELECT score FROM grades WHERE student_id = ?", (student_id,))
    else:
        if g.user['role'] == 'student':
            return jsonify({'error': '无权限'}), 403
        if g.user['role'] == 'teacher':
            tcs = query("SELECT college_code, major_code, class_name FROM teacher_classes WHERE user_id = ?",
                        (g.user['user_id'],))
            if not tcs:
                return jsonify({'avg': 0, 'max': 0, 'min': 0, 'pass_rate': 0, 'count': 0})
            conds = []
            targs = []
            for tc in tcs:
                conds.append("(s.college_code = ? AND s.major_code = ? AND SUBSTR(s.student_no, 7, 2) = ?)")
                targs.extend([tc['college_code'], tc['major_code'], tc['class_name']])
            grades = query(
                "SELECT g.score FROM grades g JOIN students s ON g.student_id = s.id WHERE " + " OR ".join(conds),
                targs
            )
        else:
            grades = query("SELECT score FROM grades")

    if not grades:
        return jsonify({'avg': 0, 'max': 0, 'min': 0, 'pass_rate': 0, 'count': 0})

    scores = [g['score'] for g in grades]
    passed = sum(1 for s in scores if s >= 60)
    return jsonify({
        'avg': round(sum(scores) / len(scores), 1),
        'max': max(scores),
        'min': min(scores),
        'pass_rate': round(passed / len(scores) * 100, 1),
        'count': len(scores)
    })
