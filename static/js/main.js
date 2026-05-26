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

    // Show username with icon hint
    var userHtml = '<i class="fas fa-user-circle mr-1"></i>' + user.username + ' <i class="fas fa-pencil-alt" style="font-size:0.7rem;opacity:0.5;"></i>';
    $('#user-display').html(userHtml);
    $('#sidebar-user-display').html(userHtml);

    // Profile click handler
    function openProfile(e) {
        e.preventDefault();
        var u = JSON.parse(localStorage.getItem('user') || '{}');
        $('#profile-username').val(u.username);
        $('#profile-role').val(u.role === 'admin' ? '管理员' : u.role === 'teacher' ? '教师' : '学生');
        $('#profile-old-pw, #profile-new-pw, #profile-confirm-pw').val('');
        $('#profile-modal .field-error').text('');
        $('#profile-modal').modal('show');
    }
    $('#user-display').off('click').on('click', openProfile);
    $('#sidebar-user-display').off('click').on('click', openProfile);

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

// Profile save handler (bound on document ready)
$(function() {
    $('#btn-save-profile').on('click', function() {
        var user = JSON.parse(localStorage.getItem('user') || '{}');
        var newName = $('#profile-username').val().trim();
        var oldPw = $('#profile-old-pw').val();
        var newPw = $('#profile-new-pw').val();
        var confirmPw = $('#profile-confirm-pw').val();

        var changingPw = oldPw || newPw || confirmPw;
        var changingName = newName !== user.username;

        $('#profile-modal .field-error').text('');

        if (!newName) { $('#err-username').text('请输入用户名'); return; }
        if (!changingName && !changingPw) { $('#err-username').text('没有修改任何内容'); return; }

        var ok = true;
        if (changingPw) {
            if (!oldPw) { $('#err-old-pw').text('请输入原密码'); ok = false; }
            if (!newPw) { $('#err-new-pw').text('请输入新密码'); ok = false; }
            if (!confirmPw) { $('#err-confirm-pw').text('请确认新密码'); ok = false; }
            if (newPw && newPw.length < 6) { $('#err-new-pw').text('新密码至少6位'); ok = false; }
            if (newPw && confirmPw && newPw !== confirmPw) { $('#err-confirm-pw').text('两次密码不一致'); ok = false; }
        }
        if (!ok) return;

        var promises = [];
        var msgs = [];

        if (changingName) {
            promises.push(api.updateProfile({ username: newName }).then(function(res) {
                msgs.push(res.message);
                user.username = newName;
                localStorage.setItem('user', JSON.stringify(user));
                var newHtml = '<i class="fas fa-user-circle mr-1"></i>' + newName + ' <i class="fas fa-pencil-alt" style="font-size:0.7rem;opacity:0.5;"></i>';
                $('#user-display, #sidebar-user-display').html(newHtml);
            }));
        }

        if (changingPw) {
            promises.push(api.changePassword({ old_password: oldPw, new_password: newPw }).then(function(res) {
                msgs.push(res.message);
            }));
        }

        $.when.apply($, promises).then(function() {
            alert(msgs.join('；'));
            $('#profile-modal').modal('hide');
        }).fail(function(xhr) {
            var msg = (xhr.responseJSON && xhr.responseJSON.error) || '操作失败';
            alert(msg);
        });
    });
});
