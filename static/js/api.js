var api = {
    request: function(method, url, data) {
        return $.ajax({
            url: url,
            method: method,
            contentType: 'application/json',
            data: data ? JSON.stringify(data) : undefined,
            beforeSend: function(xhr) {
                var token = localStorage.getItem('token');
                if (token) xhr.setRequestHeader('Authorization', 'Bearer ' + token);
            },
            error: function(xhr) {
                if (xhr.status === 401) {
                    localStorage.clear();
                    window.location.href = '/login';
                }
            }
        });
    },

    get: function(url, params) {
        if (params) url += '?' + $.param(params);
        return this.request('GET', url);
    },

    post: function(url, data) { return this.request('POST', url, data); },
    put: function(url, data) { return this.request('PUT', url, data); },
    del: function(url) { return this.request('DELETE', url); },

    // Students
    getStudents: function(params) { return this.get('/api/students', params); },
    addStudent: function(data) { return this.post('/api/students', data); },
    updateStudent: function(id, data) { return this.put('/api/students/' + id, data); },
    deleteStudent: function(id) { return this.del('/api/students/' + id); },
    getMyInfo: function() { return this.get('/api/students/me'); },

    // Grades
    getGrades: function(params) { return this.get('/api/grades', params); },
    addGrade: function(data) { return this.post('/api/grades', data); },
    updateGrade: function(id, data) { return this.put('/api/grades/' + id, data); },
    deleteGrade: function(id) { return this.del('/api/grades/' + id); },

    // Courses & Colleges
    getCourses: function(params) { return this.get('/api/courses', params); },
    addCourse: function(data) { return this.post('/api/courses', data); },
    updateCourse: function(id, data) { return this.put('/api/courses/' + id, data); },
    deleteCourse: function(id) { return this.del('/api/courses/' + id); },
    getColleges: function() { return this.get('/api/colleges'); },
    addCollege: function(data) { return this.post('/api/colleges', data); },
    updateCollege: function(code, data) { return this.put('/api/colleges/' + code, data); },
    deleteCollege: function(code) { return this.del('/api/colleges/' + code); },
    getMajors: function(params) { return this.get('/api/majors', params); },
    addMajor: function(data) { return this.post('/api/majors', data); },
    updateMajor: function(id, data) { return this.put('/api/majors/' + id, data); },
    deleteMajor: function(id) { return this.del('/api/majors/' + id); },
    getNextStudentNo: function(params) { return this.get('/api/students/next-no', params); },
    getClasses: function(params) { return this.get('/api/students/classes', params); },

    // Teachers
    getTeachers: function(params) { return this.get('/api/teachers', params); },
    addTeacher: function(data) { return this.post('/api/teachers', data); },
    updateTeacher: function(id, data) { return this.put('/api/teachers/' + id, data); },
    deleteTeacher: function(id) { return this.del('/api/teachers/' + id); },
    getMyClasses: function() { return this.get('/api/teachers/me/classes'); },

    // Auth
    updateProfile: function(data) { return this.put('/api/me', data); },
    changePassword: function(data) { return this.put('/api/me/password', data); },

    // Schedules
    getSchedules: function(params) { return this.get('/api/schedules', params); },
    saveSchedules: function(data) { return this.put('/api/schedules', data); },
    getScheduleClasses: function() { return this.get('/api/schedules/classes'); },

    // Stats & Years
    getStats: function(params) { return this.get('/api/grades/stats', params); },
    getYears: function() { return this.get('/api/grades/years'); },
    exportGrades: function(params) { return this.get('/api/grades/export', params); },
    exportStudents: function(params) { return this.get('/api/students/export', params); }
};
