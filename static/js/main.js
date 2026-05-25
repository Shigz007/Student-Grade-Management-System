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
    $('#user-display').html('<i class="fas fa-user-circle mr-1"></i>' + user.username + ' <i class="fas fa-pencil-alt" style="font-size:0.7rem;opacity:0.5;"></i>');

    // Profile click handler
    $('#user-display').off('click').on('click', function(e) {
        e.preventDefault();
        var u = JSON.parse(localStorage.getItem('user') || '{}');
        $('#profile-username').val(u.username);
        $('#profile-role').val(u.role === 'admin' ? '管理员' : u.role === 'teacher' ? '教师' : '学生');
        $('#profile-old-pw, #profile-new-pw, #profile-confirm-pw').val('');
        $('#profile-modal').modal('show');
    });

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

        if (!newName) { alert('用户名不能为空'); return; }

        var changingPw = oldPw || newPw || confirmPw;
        var changingName = newName !== user.username;

        if (!changingName && !changingPw) { alert('没有修改任何内容'); return; }

        if (changingPw) {
            if (!oldPw || !newPw || !confirmPw) { alert('请填写所有密码字段'); return; }
            if (newPw.length < 6) { alert('新密码长度不能少于6位'); return; }
            if (newPw !== confirmPw) { alert('两次输入的新密码不一致'); return; }
        }

        var promises = [];
        var msgs = [];

        if (changingName) {
            promises.push(api.updateProfile({ username: newName }).then(function(res) {
                msgs.push(res.message);
                user.username = newName;
                localStorage.setItem('user', JSON.stringify(user));
                $('#user-display').html('<i class="fas fa-user-circle mr-1"></i>' + newName + ' <i class="fas fa-pencil-alt" style="font-size:0.7rem;opacity:0.5;"></i>');
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
