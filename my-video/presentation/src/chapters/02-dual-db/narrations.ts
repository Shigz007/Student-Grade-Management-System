const narrations: string[] = [
  "数据库用了两个。一个叫 data.db，一个叫 school.db。",
  "用户表、学生表、成绩表放一个库。",
  "学院、专业、课程放另一个库。",
  "靠一句 ATTACH DATABASE，把 school.db 挂到 data.db 的连接上。",
  "然后一条 SQL 就能直接跨库 JOIN 查询。学号、姓名、课程名、学院名、分数、学期，一锅出。",
];

export { narrations };
