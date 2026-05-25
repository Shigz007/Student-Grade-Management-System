CREATE TABLE IF NOT EXISTS colleges (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS majors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    college_code TEXT NOT NULL,
    FOREIGN KEY (college_code) REFERENCES colleges(code),
    UNIQUE(college_code, code)
);

CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    college_code TEXT NOT NULL,
    major_code TEXT DEFAULT '',
    FOREIGN KEY (college_code) REFERENCES colleges(code)
);
