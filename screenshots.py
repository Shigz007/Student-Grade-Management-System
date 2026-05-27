"""Capture screenshots of all pages using Playwright."""
import os
import sys
import io
import time
import subprocess
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE = os.path.dirname(os.path.abspath(__file__))
SCREENSHOTS = os.path.join(BASE, 'screenshots')
BASE_URL = 'http://localhost:5000'

# Pages to capture: (filename, path, login_role)
PAGES = {
    'admin': [
        ('admin-dashboard', '/admin'),
        ('admin-students', '/admin/students'),
        ('admin-grades', '/admin/grades'),
        ('admin-teachers', '/admin/teachers'),
        ('admin-schedules', '/admin/schedules'),
        ('admin-courses', '/admin/courses'),
    ],
    'teacher': [
        ('teacher-dashboard', '/teacher'),
        ('teacher-students', '/teacher/students'),
        ('teacher-grades', '/teacher/grades'),
        ('teacher-schedules', '/teacher/schedules'),
    ],
    'student': [
        ('student-dashboard', '/student'),
        ('student-grades', '/student/grades'),
    ],
}

# Look up a real student name from the DB
sys.path.insert(0, BASE)
from db import query
student_row = query("SELECT name FROM students LIMIT 1", one=True)
STUDENT_NAME = student_row['name'] if student_row else '学生'
print(f'Using student account: {STUDENT_NAME}')

CREDENTIALS = {
    'admin': ('admin', 'admin123'),
    'teacher': ('teacher', 'teacher123'),
    'student': (STUDENT_NAME, 'Ad112233'),
}

def login(page, role):
    username, password = CREDENTIALS[role]
    page.goto(f'{BASE_URL}/login')
    page.wait_for_selector('#username', timeout=10000)
    page.fill('#username', username)
    page.fill('#password', password)
    page.click('button[type="submit"]')
    page.wait_for_url(f'{BASE_URL}{"/" + role}', timeout=10000)
    time.sleep(1.5)

def capture_page(page, filename, path):
    filepath = os.path.join(SCREENSHOTS, f'{filename}.png')
    page.goto(f'{BASE_URL}{path}')
    try:
        page.wait_for_load_state('networkidle', timeout=15000)
    except:
        pass
    time.sleep(1)
    page.screenshot(path=filepath, full_page=False)
    print(f'  OK {filename}.png')

def main():
    print('Starting Flask server...')
    server = subprocess.Popen(
        [sys.executable, 'app.py'],
        cwd=BASE,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(2)

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)

        # Login page - fresh context
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        page.goto(f'{BASE_URL}/login')
        page.wait_for_selector('#username', timeout=10000)
        time.sleep(0.5)
        page.screenshot(path=os.path.join(SCREENSHOTS, 'login.png'), full_page=False)
        ctx.close()
        print('OK login.png')

        for role, pages in PAGES.items():
            print(f'\n--- [{role}] ---')
            ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
            page = ctx.new_page()
            login(page, role)
            for filename, path in pages:
                capture_page(page, filename, path)
            ctx.close()

        browser.close()

    print('\nKilling server...')
    server.terminate()
    server.wait()
    print('Done!')

if __name__ == '__main__':
    main()
