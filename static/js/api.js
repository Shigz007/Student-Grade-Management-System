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

    // Grades
    getGrades: function(params) { return this.get('/api/grades', params); },
    addGrade: function(data) { return this.post('/api/grades', data); },
    updateGrade: function(id, data) { return this.put('/api/grades/' + id, data); },
    deleteGrade: function(id) { return this.del('/api/grades/' + id); },

    // Stats
    getStats: function(params) { return this.get('/api/grades/stats', params); }
};
