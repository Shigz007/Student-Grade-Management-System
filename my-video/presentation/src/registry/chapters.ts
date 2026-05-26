import type { ChapterDef } from "./types";
import ColdopenChapter from "../chapters/01-coldopen/Coldopen";
import { narrations as coldopenNarrations } from "../chapters/01-coldopen/narrations";
import DualDbChapter from "../chapters/02-dual-db/DualDb";
import { narrations as dualDbNarrations } from "../chapters/02-dual-db/narrations";
import RolesChapter from "../chapters/03-roles/Roles";
import { narrations as rolesNarrations } from "../chapters/03-roles/narrations";
import StudentIdChapter from "../chapters/04-student-id/StudentId";
import { narrations as studentIdNarrations } from "../chapters/04-student-id/narrations";
import GradeSearchChapter from "../chapters/05-grade-search/GradeSearch";
import { narrations as gradeSearchNarrations } from "../chapters/05-grade-search/narrations";
import DashboardWrapupChapter from "../chapters/06-dashboard-wrapup/DashboardWrapup";
import { narrations as dashboardWrapupNarrations } from "../chapters/06-dashboard-wrapup/narrations";

export const CHAPTERS: ChapterDef[] = [
  { id: "coldopen", title: "系统初见", narrations: coldopenNarrations, Component: ColdopenChapter },
  { id: "dual-db", title: "双数据库架构", narrations: dualDbNarrations, Component: DualDbChapter },
  { id: "roles", title: "三角色权限", narrations: rolesNarrations, Component: RolesChapter },
  { id: "student-id", title: "学号自动生成", narrations: studentIdNarrations, Component: StudentIdChapter },
  { id: "grade-search", title: "成绩管理 & 模糊搜索", narrations: gradeSearchNarrations, Component: GradeSearchChapter },
  { id: "dashboard-wrapup", title: "仪表盘 & 开箱即用", narrations: dashboardWrapupNarrations, Component: DashboardWrapupChapter },
];
