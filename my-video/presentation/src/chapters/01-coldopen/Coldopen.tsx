import type { ChapterStepProps } from "../../registry/types";

const W: React.CSSProperties = {
  position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
  alignItems: 'center', justifyContent: 'center', padding: '80px 100px',
  fontFamily: '"IBM Plex Sans", "Noto Serif SC", "Microsoft YaHei", sans-serif', color: '#0a1f3d',
};

export default function Coldopen({ step }: ChapterStepProps) {
  return (
    <div style={W}>
      {step === 0 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ width: 360, height: 1, background: '#d1d5db', margin: '0 auto 60px' }} />
          <h1 style={{ fontSize: 140, fontWeight: 200, letterSpacing: '-0.02em', lineHeight: 1.1, margin: 0 }}>
            一个系统<span style={{ color: '#1e3a8a' }}>，</span>管全校成绩
          </h1>
          <div style={{ width: 520, height: 1, background: '#d1d5db', margin: '60px auto 0' }} />
        </div>
      )}

      {step === 1 && (
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: 72, fontWeight: 200, color: '#0a1f3d', opacity: 0.35, margin: '0 0 56px' }}>
            一个系统，管全校成绩
          </h2>
          <p style={{ fontSize: 52, color: '#64748b', textDecoration: 'line-through', textDecorationColor: '#1e3a8a', margin: '0 0 32px' }}>
            几十万的教务系统
          </p>
          <p style={{ fontSize: 80, fontWeight: 300, color: '#0a1f3d', margin: 0 }}>
            一个人<span style={{ color: '#1e3a8a', fontWeight: 600 }}>就能</span>搭起来
          </p>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: 56, fontWeight: 200, color: '#0a1f3d', opacity: 0.3, margin: '0 0 100px' }}>
            一个系统，管全校成绩
          </h2>
          <div style={{ display: 'flex', gap: 80 }}>
            {[
              { name: 'Flask', label: '轻量后端' },
              { name: 'SQLite', label: '双库分离' },
              { name: 'Bootstrap 4', label: '响应式 UI' },
            ].map((t) => (
              <div key={t.name} style={{ textAlign: 'center' }}>
                <div style={{
                  padding: '28px 56px', border: '1px solid #1e3a8a',
                  fontSize: 36, fontFamily: '"JetBrains Mono", "Consolas", monospace',
                  color: '#1e3a8a', marginBottom: 16,
                }}>{t.name}</div>
                <div style={{ fontSize: 24, color: '#64748b', letterSpacing: '0.06em' }}>{t.label}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {step === 3 && (
        <div style={{ textAlign: 'center' }}>
          <h2 style={{ fontSize: 64, fontWeight: 200, color: '#0a1f3d', opacity: 0.4, margin: '0 0 80px' }}>
            开箱即用，拿来就能跑
          </h2>
          <div style={{ width: 200, height: 1, background: '#d1d5db', margin: '0 auto 64px' }} />
          <div style={{ display: 'flex', gap: 64, alignItems: 'center' }}>
            {[
              ['11', '学院'],
              ['28', '专业'],
              ['238', '课程'],
              ['1729', '学生'],
            ].map(([num, label], i, arr) => (
              <div key={label} style={{ display: 'flex', alignItems: 'center', gap: 64 }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: 96, fontWeight: 200, color: '#1e3a8a', fontFamily: '"Playfair Display", "Noto Serif SC", serif', lineHeight: 1 }}>
                    {num}
                  </div>
                  <div style={{ fontSize: 24, color: '#1a3050', letterSpacing: '0.08em', marginTop: 10 }}>
                    {label}
                  </div>
                </div>
                {i < arr.length - 1 && (
                  <div style={{ width: 1, height: 56, background: '#d1d5db' }} />
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
