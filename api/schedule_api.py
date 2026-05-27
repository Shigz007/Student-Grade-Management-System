from flask import Blueprint, request, jsonify, g
from auth import login_required, admin_required
from db import query, execute

schedule_bp = Blueprint('schedule', __name__)

TIME_SLOTS = [
    '08:30-10:05',
    '10:25-12:00',
    '13:30-15:05',
    '15:25-17:00',
    '17:10-18:45',
    '19:00-20:25',
]


@schedule_bp.route('/api/schedules', methods=['GET'])
@login_required
def get_schedules():
    college_code = request.args.get('college_code', '').strip()
    major_code = request.args.get('major_code', '').strip()
    class_name = request.args.get('class_name', '').strip()

    if not college_code or not major_code or not class_name:
        return jsonify({'error': '请选择学院、专业和班级'}), 400

    rows = query(
        """SELECT s.*, c.name AS course_name, c.code AS course_code
           FROM schedules s
           JOIN school.courses c ON s.course_id = c.id
           WHERE s.college_code = ? AND s.major_code = ? AND s.class_name = ?
           ORDER BY s.day_of_week, s.time_slot""",
        (college_code, major_code, class_name)
    )
    return jsonify([{
        'id': r['id'],
        'day_of_week': r['day_of_week'],
        'time_slot': r['time_slot'],
        'course_id': r['course_id'],
        'course_name': r['course_name'],
        'course_code': r['course_code'],
    } for r in rows])


@schedule_bp.route('/api/schedules', methods=['PUT'])
@admin_required
def save_schedules():
    data = request.get_json()
    college_code = data.get('college_code', '').strip()
    major_code = data.get('major_code', '').strip()
    class_name = data.get('class_name', '').strip()
    entries = data.get('entries', [])

    if not college_code or not major_code or not class_name:
        return jsonify({'error': '请选择学院、专业和班级'}), 400

    execute(
        "DELETE FROM schedules WHERE college_code = ? AND major_code = ? AND class_name = ?",
        (college_code, major_code, class_name)
    )

    count = 0
    for entry in entries:
        course_id = entry.get('course_id')
        day_of_week = entry.get('day_of_week')
        time_slot = entry.get('time_slot')
        if not course_id or not day_of_week or not time_slot:
            continue
        execute(
            "INSERT INTO schedules (college_code, major_code, class_name, day_of_week, time_slot, course_id) VALUES (?,?,?,?,?,?)",
            (college_code, major_code, class_name, int(day_of_week), int(time_slot), int(course_id))
        )
        count += 1

    return jsonify({'message': '保存成功', 'count': count})


@schedule_bp.route('/api/schedules/classes', methods=['GET'])
@login_required
def get_schedule_classes():
    if g.user['role'] == 'teacher':
        rows = query(
            """SELECT DISTINCT tc.college_code, cl.name AS college_name,
                      tc.major_code, m.name AS major_name,
                      tc.class_name
               FROM teacher_classes tc
               JOIN school.colleges cl ON tc.college_code = cl.code
               JOIN school.majors m ON tc.college_code = m.college_code AND tc.major_code = m.code
               WHERE tc.user_id = ?
               ORDER BY tc.college_code, tc.major_code, tc.class_name""",
            (g.user['user_id'],)
        )
    else:
        rows = query(
            """SELECT DISTINCT s.college_code, cl.name AS college_name,
                      s.major_code, m.name AS major_name,
                      s.class_name
               FROM students s
               JOIN school.colleges cl ON s.college_code = cl.code
               JOIN school.majors m ON s.college_code = m.college_code AND s.major_code = m.code
               WHERE s.class_name != ''
               ORDER BY s.college_code, s.major_code, s.class_name"""
        )
    return jsonify([{
        'college_code': r['college_code'],
        'college_name': r['college_name'],
        'major_code': r['major_code'],
        'major_name': r['major_name'],
        'class_name': r['class_name'],
    } for r in rows])
