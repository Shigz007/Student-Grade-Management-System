import type { ChapterStepProps } from "../../registry/types";

const W: React.CSSProperties = {
  position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
  alignItems: 'center', justifyContent: 'center', padding: '80px 100px',
  fontFamily: '"IBM Plex Sans", "Noto Serif SC", "Microsoft YaHei", sans-serif', color: '#0a1f3d',
};
const mono = '"JetBrains Mono", "Consolas", monospace';
const accent = '#1e3a8a';
const mute = '#64748b';

export default function DualDb({ step }: ChapterStepProps) {
  return (
    <div style={W}>
      {step === 0 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 52 }}>
            Architecture
          </div>
          <div style={{ display: 'flex', gap: 160 }}>
            {[
              ['data.db', '用户数据'],
              ['school.db', '学校数据'],
            ].map(([name, sub]) => (
              <div key={name} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 24 }}>
                <div style={{
                  width: 200, height: 200, border: '1px solid #0a1f3d',
                  display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative',
                }}>
                  <div style={{ position: 'absolute', top: 36, left: '50%', width: 100, height: 1, background: '#0a1f3d', transform: 'translateX(-50%)' }} />
                  <div style={{ position: 'absolute', top: 72, left: '50%', width: 76, height: 1, background: '#0a1f3d', transform: 'translateX(-50%)' }} />
                </div>
                <div style={{ fontFamily: mono, fontSize: 32, color: accent, fontWeight: 500 }}>{name}</div>
                <div style={{ fontSize: 22, color: mute, letterSpacing: '0.06em' }}>{sub}</div>
              </div>
            ))}
          </div>
        </>
      )}

      {step === 1 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 28, color: accent, fontWeight: 500, marginBottom: 40, letterSpacing: '0.04em' }}>
            data.db
          </div>
          <div style={{ display: 'flex', gap: 24 }}>
            {['users', 'students', 'grades'].map((t) => (
              <div key={t} style={{ padding: '28px 48px', border: '1px solid #0a1f3d', background: '#f1f3f5', fontFamily: mono, fontSize: 24, color: '#0a1f3d', letterSpacing: '0.03em', textAlign: 'center' }}>
                <div style={{ fontSize: 14, color: mute, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 6 }}>Table</div>
                {t}
              </div>
            ))}
          </div>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ opacity: 0.25, marginBottom: 64 }}>
            <div style={{ fontFamily: mono, fontSize: 20, color: accent, fontWeight: 500, marginBottom: 24, letterSpacing: '0.04em' }}>data.db</div>
            <div style={{ display: 'flex', gap: 16 }}>
              {['users', 'students', 'grades'].map((t) => (
                <div key={t} style={{ padding: '16px 28px', border: '1px solid #0a1f3d', fontFamily: mono, fontSize: 18, color: '#0a1f3d' }}>{t}</div>
              ))}
            </div>
          </div>
          <div>
            <div style={{ fontFamily: mono, fontSize: 28, color: accent, fontWeight: 500, marginBottom: 40, letterSpacing: '0.04em' }}>school.db</div>
            <div style={{ display: 'flex', gap: 24 }}>
              {['colleges', 'majors', 'courses'].map((t) => (
                <div key={t} style={{ padding: '28px 48px', border: '1px solid #1e3a8a', background: '#f1f3f5', fontFamily: mono, fontSize: 24, color: accent, letterSpacing: '0.03em', textAlign: 'center' }}>
                  <div style={{ fontSize: 14, color: mute, textTransform: 'uppercase', letterSpacing: '0.12em', marginBottom: 6 }}>Table</div>
                  {t}
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {step === 3 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 48 }}>
            ATTACH DATABASE
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 0 }}>
            <div style={{ padding: '28px 52px', border: '1px solid #0a1f3d', fontFamily: mono, fontSize: 28, background: '#f1f3f5' }}>
              <span style={{ color: accent }}>data</span>.db
            </div>
            <div style={{ width: 160, display: 'flex', alignItems: 'center' }}>
              <div style={{ flex: 1, height: 1, background: accent }} />
              <div style={{ width: 8, height: 8, borderRadius: '50%', background: accent, marginLeft: -4 }} />
            </div>
            <div style={{ padding: '28px 52px', border: '1px solid #0a1f3d', fontFamily: mono, fontSize: 28, background: '#f1f3f5' }}>
              <span style={{ color: accent }}>school</span>.db
            </div>
          </div>
          <div style={{ fontFamily: mono, fontSize: 16, color: accent, letterSpacing: '0.1em', marginTop: 18 }}>
            ATTACH AS school
          </div>
        </>
      )}

      {step === 4 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 36 }}>
            Cross-DB JOIN Query
          </div>
          <div style={{ border: '1px solid #0a1f3d', padding: '32px 48px', background: '#f1f3f5', maxWidth: 1000 }}>
            {[
              ['SELECT', ' s.student_no, s.name, c.name AS course_name,'],
              ['', '       cl.name AS college_name, g.score, g.semester_year'],
              ['FROM', ' grades g'],
              ['JOIN', ' students s ON g.student_id = s.id'],
              ['JOIN', ' courses c ON g.course_id = c.id'],
              ['JOIN', ' colleges cl ON c.college_code = cl.code'],
            ].map(([kw, rest], i) => (
              <div key={i} style={{ fontFamily: mono, fontSize: 22, lineHeight: 1.9, letterSpacing: '0.02em' }}>
                {kw && <span style={{ color: accent, fontWeight: 500 }}>{kw}</span>}
                <span style={{ color: kw ? '#0a1f3d' : mute }}>{rest}</span>
              </div>
            ))}
          </div>
          <div style={{ display: 'flex', gap: 40, marginTop: 36 }}>
            {[
              ['2026010101', '学号'],
              ['张三', '姓名'],
              ['计算机组成原理', '课程'],
              ['计算机学院', '学院'],
              ['89', '分数'],
            ].map(([val, col]) => (
              <div key={col} style={{ textAlign: 'center' }}>
                <div style={{ fontFamily: mono, fontSize: 18, color: '#0a1f3d' }}>{val}</div>
                <div style={{ fontSize: 14, color: mute, textTransform: 'uppercase', letterSpacing: '0.1em', marginTop: 4 }}>{col}</div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
