import type { ChapterStepProps } from "../../registry/types";

const W: React.CSSProperties = {
  position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
  alignItems: 'center', justifyContent: 'center', padding: '80px 100px',
  fontFamily: '"IBM Plex Sans", "Noto Serif SC", "Microsoft YaHei", sans-serif', color: '#0a1f3d',
};
const mono = '"JetBrains Mono", "Consolas", monospace';
const accent = '#1e3a8a';
const mute = '#64748b';

export default function GradeSearch({ step }: ChapterStepProps) {
  return (
    <div style={W}>
      {step === 0 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 48 }}>
            Grade Entry
          </div>
          <div style={{ display: 'flex', gap: 24, alignItems: 'center' }}>
            {['选学期', '选课程', '选学生', '填分数'].map((s, i, arr) => (
              <div key={s} style={{ display: 'flex', alignItems: 'center', gap: 24 }}>
                <div style={{ padding: '24px 48px', border: '1px solid #0a0a0a', fontSize: 28, background: '#f1f3f5' }}>{s}</div>
                {i < arr.length - 1 && <span style={{ color: '#d1d5db', fontSize: 24 }}>→</span>}
              </div>
            ))}
          </div>
          <div style={{ fontSize: 22, color: mute, marginTop: 32 }}>
            分数范围 0–100 · 管理员录全校 · 教师录本院
          </div>
        </>
      )}

      {step === 1 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 44 }}>
            Fuzzy Search
          </div>
          <div style={{
            padding: '28px 64px', border: '1px solid #002fa7',
            fontSize: 40, fontFamily: mono, color: '#0a1f3d', marginBottom: 24,
          }}>计算机刘佳</div>
          <div style={{ fontSize: 24, color: mute }}>中英文混合，5 个字</div>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 36 }}>
            Regex Tokenization
          </div>
          <div style={{ fontSize: 18, color: mute, fontFamily: mono, marginBottom: 24, wordBreak: 'break-all' }}>
            re.findall(r'[一-鿿]|[^一-鿿]+', part)
          </div>
          <div style={{ display: 'flex', gap: 16, marginBottom: 24 }}>
            {['计', '算', '机'].map((c) => (
              <div key={c} style={{ width: 64, height: 64, border: '1px solid #002fa7', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32, color: accent }}>{c}</div>
            ))}
          </div>
          <div style={{ fontSize: 16, color: mute, marginBottom: 28 }}>中文 → 逐字拆分</div>
          <div style={{ display: 'flex', gap: 16 }}>
            {['刘', '佳'].map((c) => (
              <div key={c} style={{ width: 64, height: 64, border: '1px solid #002fa7', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32, color: accent }}>{c}</div>
            ))}
          </div>
          <div style={{ fontSize: 16, color: mute, marginTop: 8 }}>保持连续</div>
        </div>
      )}

      {step === 3 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 32 }}>
            Token Matching
          </div>
          <div style={{ display: 'flex', gap: 14, marginBottom: 44 }}>
            {['计', '算', '机', '刘', '佳'].map((t) => (
              <div key={t} style={{ width: 56, height: 56, border: '1px solid #002fa7', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 28, color: accent, fontFamily: mono }}>{t}</div>
            ))}
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16, fontSize: 22 }}>
            {[
              ['学号', '2026010101'],
              ['姓名', '刘佳'],
              ['课程', '计算机组成原理'],
              ['学院', '计算机学院'],
            ].map(([field, sample]) => (
              <div key={field} style={{ display: 'flex', gap: 32, justifyContent: 'center', alignItems: 'center' }}>
                <div style={{ width: 80, textAlign: 'right', color: mute, fontSize: 18 }}>{field}</div>
                <div style={{ width: 260, padding: '8px 16px', border: '1px solid #e0e0e0', textAlign: 'left', fontSize: 20, fontFamily: mono }}>{sample}</div>
                <div style={{ width: 20, height: 20, background: accent }} title="match" />
              </div>
            ))}
          </div>
          <div style={{ fontSize: 20, color: accent, marginTop: 28 }}>
            5 个 token 各自匹配所有字段 → 找到！
          </div>
        </div>
      )}

      {step === 4 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 64, fontWeight: 300, color: accent, marginBottom: 32 }}>
            任意顺序
          </div>
          <div style={{ display: 'flex', gap: 32, marginBottom: 40 }}>
            {['计算机 刘佳', '刘佳 计算机', '2020 第一学期'].map((q) => (
              <div key={q} style={{
                padding: '20px 40px', border: '1px solid #e0e0e0',
                fontSize: 26, background: '#f1f3f5', fontFamily: mono,
              }}>{q}</div>
            ))}
          </div>
          <div style={{ fontSize: 28, fontWeight: 300 }}>
            不管先输什么<span style={{ color: accent }}>，</span>都能搜到
          </div>
        </div>
      )}

      {step === 5 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 40 }}>
            Semester Matching
          </div>
          <div style={{ display: 'flex', gap: 24, alignItems: 'center', marginBottom: 32 }}>
            <div style={{ padding: '20px 40px', border: '1px solid #0a0a0a', fontSize: 28 }}>第一学期</div>
            <span style={{ fontSize: 28, color: '#d1d5db' }}>→</span>
            <div style={{ padding: '20px 40px', border: '1px solid #002fa7', fontSize: 28 }}>
              <span style={{ color: mute }}>第</span>
              <span style={{ color: accent }}>1</span>
              <span style={{ color: mute }}>学期</span>
            </div>
          </div>
          <div style={{ fontSize: 20, color: mute, maxWidth: 600, lineHeight: 1.7 }}>
            数据库拼成 "第X学期" 格式匹配，支持中文数字转换
          </div>
        </div>
      )}
    </div>
  );
}
