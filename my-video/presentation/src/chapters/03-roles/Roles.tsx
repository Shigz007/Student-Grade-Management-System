import type { ChapterStepProps } from "../../registry/types";

const W: React.CSSProperties = {
  position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
  alignItems: 'center', justifyContent: 'center', padding: '80px 100px',
  fontFamily: '"IBM Plex Sans", "Noto Serif SC", "Microsoft YaHei", sans-serif', color: '#0a1f3d',
};
const mono = '"JetBrains Mono", "Consolas", monospace';
const accent = '#1e3a8a';
const mute = '#64748b';

export default function Roles({ step }: ChapterStepProps) {
  return (
    <div style={W}>
      {step === 0 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 60 }}>
            Role-Based Access
          </div>
          <div style={{ display: 'flex', gap: 48, alignItems: 'center' }}>
            {[
              ['管理员', 'Admin'],
              ['教师', 'Teacher'],
              ['学生', 'Student'],
            ].map(([role, perm], i, arr) => (
              <div key={role} style={{ display: 'flex', alignItems: 'center', gap: 48 }}>
                <div style={{ padding: '40px 64px', border: '1px solid #002fa7', background: 'rgba(30,58,138,0.03)', textAlign: 'center' }}>
                  <div style={{ fontSize: 40, fontWeight: 300, color: accent, marginBottom: 12 }}>{role}</div>
                  <div style={{ fontSize: 20, color: mute, letterSpacing: '0.06em' }}>{perm}</div>
                </div>
                {i < arr.length - 1 && <div style={{ color: '#d1d5db', fontSize: 28 }}>+</div>}
              </div>
            ))}
          </div>
        </>
      )}

      {step === 1 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 52 }}>
            Permission Scope
          </div>
          <div style={{ display: 'flex', gap: 48, alignItems: 'stretch' }}>
            <div style={{ padding: '48px 56px', border: '1px solid #002fa7', background: 'rgba(30,58,138,0.03)', textAlign: 'center' }}>
              <div style={{ fontSize: 36, fontWeight: 300, color: accent, marginBottom: 28 }}>管理员</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {['全校学生', '全部成绩', '所有学院', '仪表盘'].map((s) => (
                  <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 12, justifyContent: 'center' }}>
                    <div style={{ width: 8, height: 8, background: accent }} />
                    <span style={{ fontSize: 22, color: '#0a1f3d' }}>{s}</span>
                  </div>
                ))}
              </div>
            </div>
            <div style={{ padding: '48px 56px', border: '1px solid #e0e0e0', textAlign: 'center', opacity: 0.5 }}>
              <div style={{ fontSize: 36, fontWeight: 300, marginBottom: 28 }}>教师</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {['本院学生', '本院成绩'].map((s) => (
                  <div key={s} style={{ fontSize: 22, color: '#0a1f3d' }}>{s}</div>
                ))}
              </div>
            </div>
            <div style={{ padding: '48px 56px', border: '1px solid #e0e0e0', textAlign: 'center', opacity: 0.3 }}>
              <div style={{ fontSize: 36, fontWeight: 300, marginBottom: 28 }}>学生</div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                {['个人成绩'].map((s) => (
                  <div key={s} style={{ fontSize: 22, color: '#0a1f3d' }}>{s}</div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 48 }}>
            JWT Authentication
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 32, marginBottom: 40 }}>
            <div style={{ padding: '24px 48px', border: '1px solid #0a0a0a', fontSize: 28 }}>登录</div>
            <div style={{ fontSize: 32, color: '#d1d5db' }}>→</div>
            <div style={{ padding: '24px 48px', border: '1px solid accent', background: 'rgba(30,58,138,0.04)' }}>
              <div style={{ fontFamily: mono, fontSize: 18, color: accent, wordBreak: 'break-all' }}>
                eyJhbGciOi...token...
              </div>
            </div>
            <div style={{ fontSize: 32, color: '#d1d5db' }}>→</div>
            <div style={{ padding: '24px 48px', border: '1px solid #0a0a0a', fontSize: 28 }}>API 请求</div>
          </div>
          <div style={{ fontSize: 22, color: mute }}>HS256 · Bearer Token · 每次请求校验</div>
        </div>
      )}

      {step === 3 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 44 }}>
            Role Decorator
          </div>
          <div style={{ border: '1px solid #0a0a0a', padding: '28px 52px', background: '#f1f3f5', fontFamily: mono, fontSize: 22, lineHeight: 1.8, marginBottom: 32 }}>
            <div><span style={{ color: accent }}>@require_role</span>(<span style={{ color: '#0a1f3d' }}>'admin', 'teacher'</span>)</div>
            <div><span style={{ color: accent }}>def</span> <span style={{ color: '#0a1f3d' }}>add_grade</span>():</div>
            <div style={{ paddingLeft: 24 }}>...</div>
          </div>
          <div style={{ display: 'flex', gap: 48 }}>
            {[
              ['/api/grades/add', 'admin / teacher'],
              ['/api/students/all', 'admin / teacher'],
              ['/api/stats/dashboard', 'admin / teacher'],
            ].map(([path, roles]) => (
              <div key={path} style={{ textAlign: 'center' }}>
                <div style={{ fontFamily: mono, fontSize: 16, color: accent, marginBottom: 6 }}>{path}</div>
                <div style={{ fontSize: 16, color: mute }}>{roles}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
