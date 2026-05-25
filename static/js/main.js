function checkAuth() {
    var token = localStorage.getItem('token');
    if (!token) {
        window.location.href = '/login';
        return false;
    }
    var user = JSON.parse(localStorage.getItem('user') || '{}');
    if (!user.role) {
        window.location.href = '/login';
        return false;
    }

    // Check if user is on the wrong role path
    var path = window.location.pathname;
    var rolePrefix = '/' + user.role;
    if (!path.startsWith(rolePrefix) && path !== '/login') {
        window.location.href = rolePrefix;
        return false;
    }

    // Show username
    $('#user-display').text(user.username);

    // Highlight active nav
    $('.navigation-link').removeClass('active');
    if (path === rolePrefix) $('#nav-dashboard').addClass('active');
    if (path === rolePrefix + '/students') $('#nav-students').addClass('active');
    if (path === rolePrefix + '/grades') $('#nav-grades').addClass('active');

    // Page title
    var titles = {};
    titles[rolePrefix] = '仪表盘';
    titles[rolePrefix + '/students'] = '学生管理';
    titles[rolePrefix + '/grades'] = '成绩管理';
    $('#page-title').text(titles[path] || '');

    return true;
}

function logout() {
    localStorage.clear();
    window.location.href = '/login';
}
