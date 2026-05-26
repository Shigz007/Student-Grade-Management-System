import type { ChapterStepProps } from "../../registry/types";

const W: React.CSSProperties = {
  position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
  alignItems: 'center', justifyContent: 'center', padding: '80px 100px',
  fontFamily: '"IBM Plex Sans", "Noto Serif SC", "Microsoft YaHei", sans-serif', color: '#0a1f3d',
};
const mono = '"JetBrains Mono", "Consolas", monospace';
const accent = '#1e3a8a';
const mute = '#64748b';

export default function StudentId({ step }: ChapterStepProps) {
  return (
    <div style={W}>
      {step === 0 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 56 }}>
            Auto-Generated Student ID
          </div>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
            {[
              { label: '年份', width: 160 },
              { label: '学院', width: 100 },
              { label: '专业', width: 100 },
              { label: '班级', width: 100 },
            ].map(({ label, width }) => (
              <div key={label} style={{ textAlign: 'center' }}>
                <div style={{
                  width, height: 100, border: '1px dashed #002fa7',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: mono, fontSize: 40, color: '#d4d4d2',
                }}>____</div>
                <div style={{ fontSize: 18, color: mute, marginTop: 12, letterSpacing: '0.06em' }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 24, color: mute, marginTop: 40 }}>
            4位 + 2位 + 2位 + 2位 = 10位学号
          </div>
        </>
      )}

      {step === 1 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ display: 'flex', gap: 12, alignItems: 'center', marginBottom: 64 }}>
            {[
              { val: '2026', label: '年份', w: 160 },
              { val: '01', label: '学院', w: 100 },
              { val: '01', label: '专业', w: 100 },
              { val: '01', label: '班级', w: 100 },
            ].map(({ val, label, w }) => (
              <div key={label} style={{ textAlign: 'center' }}>
                <div style={{
                  width: w, height: 100, border: '1px solid #002fa7',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontFamily: mono, fontSize: 40, color: accent,
                }}>{val}</div>
                <div style={{ fontSize: 18, color: mute, marginTop: 12, letterSpacing: '0.06em' }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 60, fontWeight: 200, color: accent, fontFamily: mono }}>
            2026010101
          </div>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: 64, fontWeight: 200, color: accent, fontFamily: mono, marginBottom: 56 }}>
            2026010101
          </div>
          <div style={{ display: 'flex', gap: 32, alignItems: 'center' }}>
            {['2026级', '计算机学院', '计科专业', '01班'].map((t, i, arr) => (
              <div key={t} style={{ display: 'flex', alignItems: 'center', gap: 32 }}>
                <span style={{ fontSize: 28, color: '#0a1f3d' }}>{t}</span>
                {i < arr.length - 1 && <span style={{ color: '#d1d5db', fontSize: 24 }}>→</span>}
              </div>
            ))}
          </div>
          <div style={{ fontSize: 20, color: mute, marginTop: 32 }}>
            2026 级 · 计算机学院 · 计算机科学与技术专业 · 第 1 班
          </div>
        </div>
      )}

      {step === 3 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 44 }}>
            Cascade Selection
          </div>
          <div style={{ display: 'flex', gap: 40, alignItems: 'flex-start' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ padding: '22px 44px', border: '1px solid #002fa7', fontSize: 26, marginBottom: 10 }}>选择学院</div>
              <div style={{ fontSize: 16, color: mute }}>API 加载专业列表</div>
            </div>
            <div style={{ color: '#d1d5db', fontSize: 28, paddingTop: 18 }}>→</div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ padding: '22px 44px', border: '1px solid #002fa7', fontSize: 26, marginBottom: 10 }}>选择专业</div>
              <div style={{ fontSize: 16, color: mute }}>自动计算班级序号</div>
            </div>
            <div style={{ color: '#d1d5db', fontSize: 28, paddingTop: 18 }}>→</div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ padding: '22px 44px', border: '1px solid #0a0a0a', fontSize: 26, marginBottom: 10 }}>学号生成</div>
              <div style={{ fontSize: 16, color: mute }}>自动填入，不可修改</div>
            </div>
          </div>
        </div>
      )}

      {step === 4 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 44 }}>
            Class Capacity: 40
          </div>
          <div style={{ display: 'flex', gap: 28, marginBottom: 32 }}>
            {['01班', '02班', '03班'].map((cls, i) => (
              <div key={cls} style={{
                width: 180, height: 180, border: i === 0 ? '1px solid #002fa7' : '1px solid #e0e0e0',
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                opacity: i === 2 ? 0.3 : 1,
              }}>
                <div style={{ fontSize: 48, fontWeight: 200, color: i === 0 ? accent : '#0a1f3d' }}>
                  {i === 0 ? '40' : i === 1 ? '12' : '0'}
                </div>
                <div style={{ fontSize: 18, color: mute, marginTop: 4 }}>/40</div>
                <div style={{ fontSize: 20, color: '#0a1f3d', marginTop: 12 }}>{cls}</div>
                {i === 0 && <div style={{ fontSize: 15, color: accent, marginTop: 6 }}>已满 → 进位</div>}
              </div>
            ))}
          </div>
          <div style={{ fontSize: 22, color: '#0a1f3d' }}>每班 40 人上限，满员自动跳下一班</div>
        </div>
      )}

      {step === 5 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 40 }}>
            Form Validation
          </div>
          <div style={{ border: '1px solid #e0e0e0', padding: '32px 64px', background: '#f1f3f5' }}>
            <div style={{ display: 'flex', gap: 32, marginBottom: 24 }}>
              {['姓名 *', '性别 *', '学院 *', '专业 *', '电话 *'].map((f, i) => (
                <div key={f} style={{ textAlign: 'center' }}>
                  <div style={{ padding: '12px 28px', border: '1px solid #0a0a0a', fontSize: 22, color: '#0a1f3d' }}>{f}</div>
                  {i === 3 && <div style={{ fontSize: 14, color: accent, marginTop: 6 }}>先选学院后解锁</div>}
                </div>
              ))}
            </div>
            <div style={{ fontSize: 20, color: mute }}>
              少填一个 → <span style={{ color: '#c9302c' }}>红色提示</span> → 无法提交
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
