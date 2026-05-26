import type { ChapterStepProps } from "../../registry/types";

const W: React.CSSProperties = {
  position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column',
  alignItems: 'center', justifyContent: 'center', padding: '80px 100px',
  fontFamily: '"IBM Plex Sans", "Noto Serif SC", "Microsoft YaHei", sans-serif', color: '#0a1f3d',
};
const mono = '"JetBrains Mono", "Consolas", monospace';
const accent = '#1e3a8a';
const mute = '#64748b';

export default function DashboardWrapup({ step }: ChapterStepProps) {
  return (
    <div style={W}>
      {step === 0 && (
        <>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 48 }}>
            Dashboard
          </div>
          <div style={{ display: 'flex', gap: 0, alignItems: 'flex-end', height: 280, marginBottom: 24 }}>
            {[
              { h: 220, label: '计算机', n: 312 },
              { h: 160, label: '经管', n: 228 },
              { h: 185, label: '外语', n: 198 },
              { h: 140, label: '数学', n: 176 },
              { h: 115, label: '法学', n: 145 },
              { h: 95, label: '文学', n: 132 },
              { h: 105, label: '艺术', n: 118 },
              { h: 80, label: '体育', n: 96 },
            ].map(({ h, label, n }) => (
              <div key={label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 100 }}>
                <div style={{ fontSize: 16, color: mute, fontFamily: mono, marginBottom: 6 }}>{n}</div>
                <div style={{ width: 52, height: h, background: accent, opacity: h / 220 }} />
                <div style={{ fontSize: 18, color: '#0a1f3d', marginTop: 10 }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 20, color: mute }}>ApexCharts 学院人数柱状图</div>
        </>
      )}

      {step === 1 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 44 }}>
            Score Distribution
          </div>
          <div style={{ display: 'flex', gap: 20, alignItems: 'flex-end', height: 200, marginBottom: 24 }}>
            {[
              { label: '不及格', range: '0–59', h: 50, color: '#c9302c' },
              { label: '及格', range: '60–69', h: 90, color: '#e6a817' },
              { label: '中等', range: '70–79', h: 136, color: '#5fc7e8' },
              { label: '良好', range: '80–89', h: 180, color: '#4a9eff' },
              { label: '优秀', range: '90–100', h: 130, color: accent },
            ].map(({ label, range, h, color }) => (
              <div key={label} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: 110 }}>
                <div style={{ fontSize: 22, fontWeight: 300, fontFamily: mono, marginBottom: 6 }}>{range}</div>
                <div style={{ width: 64, height: h, background: color, opacity: 0.8 }} />
                <div style={{ fontSize: 18, color: '#0a1f3d', marginTop: 12 }}>{label}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 20, color: mute }}>5 个分数段分布统计</div>
        </div>
      )}

      {step === 2 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 52 }}>
            Data Scale
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 32, maxWidth: 880 }}>
            <div style={{ padding: '36px 48px', border: '1px solid #1e3a8a', background: 'rgba(30,58,138,0.02)' }}>
              <div style={{ fontSize: 80, fontWeight: 200, color: accent, lineHeight: 1 }}>11</div>
              <div style={{ fontSize: 24, color: '#0a1f3d', marginTop: 6 }}>学院</div>
              <div style={{ fontSize: 16, color: mute, marginTop: 12, lineHeight: 1.6 }}>
                计算机 · 数学 · 物理 · 化学 · 生科 · 经管 · 外语 · 法学 · 文学 · 艺术 · 体育
              </div>
            </div>
            <div style={{ padding: '36px 48px', border: '1px solid #d1d5db' }}>
              <div style={{ fontSize: 80, fontWeight: 200, color: accent, lineHeight: 1 }}>28</div>
              <div style={{ fontSize: 24, color: '#0a1f3d', marginTop: 6 }}>专业</div>
              <div style={{ fontSize: 16, color: mute, marginTop: 12, lineHeight: 1.6 }}>
                计科 · 软工 · AI · 数学 · 统计 · 物理 · 金融 · 英语 · 法学 · 汉语言 ...
              </div>
            </div>
            <div style={{ padding: '36px 48px', border: '1px solid #d1d5db' }}>
              <div style={{ fontSize: 80, fontWeight: 200, color: accent, lineHeight: 1 }}>238</div>
              <div style={{ fontSize: 24, color: '#0a1f3d', marginTop: 6 }}>课程</div>
              <div style={{ fontSize: 16, color: mute, marginTop: 12, lineHeight: 1.6 }}>
                高数 · 线代 · 编译原理 · 机器学习 · 新闻采访 ...
              </div>
            </div>
            <div style={{ padding: '36px 48px', border: '1px solid #d1d5db' }}>
              <div style={{ fontSize: 80, fontWeight: 200, color: accent, lineHeight: 1 }}>1729</div>
              <div style={{ fontSize: 24, color: '#0a1f3d', marginTop: 6 }}>学生</div>
              <div style={{ fontSize: 16, color: mute, marginTop: 12, lineHeight: 1.6 }}>
                预置测试数据 + 成绩记录，开箱即用
              </div>
            </div>
          </div>
        </div>
      )}

      {step === 3 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 48 }}>
            Tech Stack
          </div>
          <div style={{ display: 'flex', gap: 40, marginBottom: 44 }}>
            {[
              { name: 'Flask', desc: 'Python Web' },
              { name: 'SQLite', desc: '双库存储' },
              { name: 'Bootstrap 4', desc: 'UI 框架' },
              { name: 'jQuery', desc: '交互逻辑' },
              { name: 'ApexCharts', desc: '图表可视化' },
            ].map(({ name, desc }) => (
              <div key={name} style={{ textAlign: 'center' }}>
                <div style={{ padding: '20px 36px', border: '1px solid #1e3a8a', fontFamily: mono, fontSize: 22, color: accent, marginBottom: 10 }}>{name}</div>
                <div style={{ fontSize: 16, color: mute }}>{desc}</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 20, color: mute, maxWidth: 700, lineHeight: 1.7 }}>
            Boomerang UI Kit · 前后端分离 · RESTful API · Blueprint 路由
          </div>
        </div>
      )}

      {step === 4 && (
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontFamily: mono, fontSize: 18, color: accent, letterSpacing: '0.14em', textTransform: 'uppercase', marginBottom: 48 }}>
            Get Started
          </div>
          <div style={{ border: '1px solid #0a1f3d', padding: '32px 64px', background: '#f1f3f5', fontFamily: mono, marginBottom: 44 }}>
            <div style={{ fontSize: 22, color: mute, marginBottom: 8 }}>$</div>
            <div style={{ fontSize: 24, color: '#0a1f3d', marginBottom: 18 }}>python seed.py</div>
            <div style={{ fontSize: 24, color: '#0a1f3d', marginBottom: 8 }}>python app.py</div>
            <div style={{ fontSize: 20, color: mute }}>
              Running on http://127.0.0.1:5000
            </div>
          </div>
          <div style={{ fontSize: 40, fontWeight: 200, color: '#0a1f3d', marginBottom: 12 }}>
            一个系统<span style={{ color: accent }}>，</span>管全校成绩
          </div>
          <div style={{ fontSize: 22, color: mute }}>
            Flask + SQLite · 零外部依赖 · Nginx 反代就上线
          </div>
        </div>
      )}
    </div>
  );
}
