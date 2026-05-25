function checkAuth() {
    var token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
    }
}

function logout() {
    localStorage.clear();
    window.location.href = '/login';
}

$(function() {
    var user = JSON.parse(localStorage.getItem('user') || '{}');

    // Role badge display
    var roleBadge = {
        'admin': 'danger',
        'teacher': 'primary',
        'student': 'success'
    };
    var roleLabel = {
        'admin': '管理员',
        'teacher': '教师',
        'student': '学生'
    };
    $('#user-display').html('<span class="badge badge-' + (roleBadge[user.role] || 'secondary') + '">' + (roleLabel[user.role] || user.role) + '</span> ' + user.username);

    var path = window.location.pathname;

    // Students cannot access student management page
    if (user.role === 'student') {
        $('#nav-students-item').hide();
        if (path === '/students') {
            window.location.href = '/grades';
            return;
        }
    }

    $('.navigation-link').removeClass('active');
    if (path === '/') $('#nav-dashboard').addClass('active');
    if (path === '/students') $('#nav-students').addClass('active');
    if (path === '/grades') $('#nav-grades').addClass('active');

    var titles = { '/': '仪表盘', '/students': '学生管理', '/grades': '成绩管理' };
    $('#page-title').text(titles[path] || '');
});
