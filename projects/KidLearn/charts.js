/* ===========================
   charts.js — KidLearn
   Learning DNA Radar + Mood Chart
   =========================== */

const Charts = (() => {

  /* ===== RADAR / LEARNING DNA ===== */
  function drawRadar(child) {
    const canvas = document.getElementById('dnaChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const subjects = Object.entries(child.subjects);
    const labels   = subjects.map(([k]) => k);
    const values   = subjects.map(([, v]) => Math.min(v.lessons / 15, 1)); // normalise 0-1
    const colors   = subjects.map(([, v]) => v.color);
    const n        = labels.length;
    const cx       = W / 2, cy = H / 2 + 10;
    const maxR     = Math.min(W, H) * 0.35;
    const step     = (Math.PI * 2) / n;

    const getXY = (i, r) => ({
      x: cx + r * Math.cos(step * i - Math.PI / 2),
      y: cy + r * Math.sin(step * i - Math.PI / 2),
    });

    // Theme-aware colours
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const gridColor = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.07)';
    const labelColor = isDark ? '#94A3B8' : '#7F8C8D';

    // ---- Grid rings ----
    [0.25, 0.5, 0.75, 1].forEach(frac => {
      ctx.beginPath();
      for (let i = 0; i <= n; i++) {
        const { x, y } = getXY(i % n, maxR * frac);
        i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
      }
      ctx.closePath();
      ctx.strokeStyle = gridColor;
      ctx.lineWidth = 1;
      ctx.stroke();
    });

    // ---- Spokes ----
    for (let i = 0; i < n; i++) {
      const { x, y } = getXY(i, maxR);
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(x, y);
      ctx.strokeStyle = gridColor;
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    // ---- Fill polygon ----
    ctx.beginPath();
    for (let i = 0; i < n; i++) {
      const { x, y } = getXY(i, maxR * (values[i] || 0.02));
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.fillStyle = 'rgba(108,99,255,0.18)';
    ctx.fill();
    ctx.strokeStyle = '#6C63FF';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    // ---- Data points ----
    for (let i = 0; i < n; i++) {
      const { x, y } = getXY(i, maxR * (values[i] || 0.02));
      ctx.beginPath();
      ctx.arc(x, y, 5, 0, Math.PI * 2);
      ctx.fillStyle = colors[i] || '#6C63FF';
      ctx.fill();
      ctx.strokeStyle = '#fff';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    // ---- Labels ----
    ctx.font = 'bold 11px Nunito, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    for (let i = 0; i < n; i++) {
      const { x, y } = getXY(i, maxR + 22);
      const subj = subjects[i];
      ctx.fillStyle = labelColor;
      ctx.fillText(`${subj[1].emoji} ${labels[i]}`, x, y);
    }
  }

  /* ===== MOOD vs PERFORMANCE ===== */
  function drawMoodChart(child) {
    const canvas = document.getElementById('moodChart');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    const log = (child.moodLog || []).slice(-7);
    if (log.length < 2) {
      const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
      ctx.fillStyle = isDark ? '#94A3B8' : '#7F8C8D';
      ctx.font = '13px Nunito, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText('Log your mood to see this chart!', W / 2, H / 2);
      return;
    }

    const pad = { t: 16, r: 20, b: 36, l: 40 };
    const cW = W - pad.l - pad.r;
    const cH = H - pad.t - pad.b;

    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const axisColor = isDark ? '#64748B' : '#CBD5E1';
    const labelColor = isDark ? '#94A3B8' : '#7F8C8D';

    const maxXP = Math.max(...log.map(m => m.xpThatDay), 1);
    const moods = log.map(m => m.mood);
    const xps   = log.map(m => m.xpThatDay);

    const xPos = (i) => pad.l + (i / (log.length - 1)) * cW;
    const yMood = (v) => pad.t + cH - ((v - 1) / 4) * cH;
    const yXP   = (v) => pad.t + cH - (v / maxXP) * cH;

    // ---- Grid ----
    ctx.strokeStyle = axisColor;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.l, pad.t);
    ctx.lineTo(pad.l, pad.t + cH);
    ctx.lineTo(pad.l + cW, pad.t + cH);
    ctx.stroke();

    // ---- XP line ----
    ctx.beginPath();
    xps.forEach((v, i) => i === 0 ? ctx.moveTo(xPos(i), yXP(v)) : ctx.lineTo(xPos(i), yXP(v)));
    ctx.strokeStyle = '#43D9AD';
    ctx.lineWidth = 2;
    ctx.stroke();

    // ---- Mood line ----
    ctx.beginPath();
    moods.forEach((v, i) => i === 0 ? ctx.moveTo(xPos(i), yMood(v)) : ctx.lineTo(xPos(i), yMood(v)));
    ctx.strokeStyle = '#FF9F43';
    ctx.lineWidth = 2.5;
    ctx.setLineDash([5, 3]);
    ctx.stroke();
    ctx.setLineDash([]);

    // ---- Dots + labels ----
    const moodEmojis = ['', '😢', '😕', '😐', '🙂', '😄'];
    log.forEach((entry, i) => {
      // Mood dot
      ctx.beginPath();
      ctx.arc(xPos(i), yMood(entry.mood), 5, 0, Math.PI * 2);
      ctx.fillStyle = '#FF9F43';
      ctx.fill();

      // Date label
      const d = new Date(entry.date);
      ctx.fillStyle = labelColor;
      ctx.font = '10px Nunito, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(`${d.getMonth()+1}/${d.getDate()}`, xPos(i), pad.t + cH + 18);
    });

    // ---- Legend ----
    ctx.font = 'bold 11px Nunito, sans-serif';
    ctx.fillStyle = '#FF9F43';
    ctx.fillText('Mood', pad.l + 24, pad.t + 8);
    ctx.fillStyle = '#43D9AD';
    ctx.fillText('XP', pad.l + 68, pad.t + 8);
  }

  /* ===== PROGRESS BARS ===== */
  function renderProgressBars(child) {
    const el = document.getElementById('progressBars');
    if (!el) return;
    const subjects = Object.entries(child.subjects);
    const max = Math.max(...subjects.map(([, v]) => v.lessons), 1);

    el.innerHTML = subjects.map(([name, data]) => {
      const pct = Math.round((data.lessons / Math.max(max, 10)) * 100);
      return `
        <div class="progress-item">
          <div class="progress-header">
            <span class="progress-subject">${data.emoji} ${name}</span>
            <span class="progress-pct">${data.lessons} lessons</span>
          </div>
          <div class="progress-track">
            <div class="progress-fill" style="width:${pct}%; background:${data.color}"></div>
          </div>
        </div>
      `;
    }).join('');
  }

  /* ===== HEATMAP ===== */
  function renderHeatmap(child) {
    const el = document.getElementById('heatmapGrid');
    if (!el) return;
    const subjects = Object.entries(child.subjects);
    const max = Math.max(...subjects.map(([, v]) => v.lessons), 1);

    el.innerHTML = subjects.map(([name, data]) => {
      const ratio = data.lessons / max;
      let cls = 'red', status = 'Needs Focus';
      if (ratio >= 0.6) { cls = 'green'; status = 'Great!'; }
      else if (ratio >= 0.3) { cls = 'yellow'; status = 'Getting There'; }
      return `
        <div class="heatmap-card ${cls}">
          <div class="heatmap-subject">${data.emoji} ${name}</div>
          <div>
            <div class="heatmap-status">${status}</div>
            <div style="font-size:11px;color:var(--text-muted);margin-top:4px;font-weight:600">${data.lessons} lessons</div>
          </div>
        </div>
      `;
    }).join('');
  }

  /* ===== REPORT CARD ===== */
  function renderReport(child) {
    const el = document.getElementById('reportWrap');
    if (!el) return;
    const subjects = Object.entries(child.subjects);
    const totalLessons = subjects.reduce((s, [, v]) => s + v.lessons, 0);

    const grade = (lessons) => {
      if (lessons >= 15) return 'A+';
      if (lessons >= 10) return 'A';
      if (lessons >= 7)  return 'B+';
      if (lessons >= 5)  return 'B';
      if (lessons >= 3)  return 'C';
      return 'D';
    };

    const now = new Date();
    el.innerHTML = `
      <div class="report-header">
        <h2>📋 Weekly Report Card</h2>
        <p>${child.avatar} ${child.name} · Week of ${now.toLocaleDateString('en-IN', { month: 'short', day: 'numeric', year: 'numeric' })}</p>
      </div>
      <div class="report-grid">
        ${subjects.map(([name, data]) => `
          <div class="report-subject-row">
            <div class="report-subject-info">
              <span style="font-size:24px">${data.emoji}</span>
              <div>
                <div>${name}</div>
                <div style="font-size:12px;color:var(--text-muted);font-weight:600">${data.lessons} lessons</div>
              </div>
            </div>
            <div class="report-grade">${grade(data.lessons)}</div>
          </div>
        `).join('')}
      </div>
      <div class="card" style="margin-top:16px">
        <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:12px">
          <div><div style="font-size:13px;color:var(--text-muted);font-weight:700">TOTAL LESSONS</div><div style="font-size:28px;font-weight:800;color:var(--primary)">${totalLessons}</div></div>
          <div><div style="font-size:13px;color:var(--text-muted);font-weight:700">TOTAL XP</div><div style="font-size:28px;font-weight:800;color:var(--accent-orange)">${child.xp} ⚡</div></div>
          <div><div style="font-size:13px;color:var(--text-muted);font-weight:700">BEST STREAK</div><div style="font-size:28px;font-weight:800;color:var(--secondary)">${child.streak} 🔥</div></div>
          <div><div style="font-size:13px;color:var(--text-muted);font-weight:700">BADGES</div><div style="font-size:28px;font-weight:800;color:var(--accent-green)">${(child.badges||[]).length} 🏅</div></div>
        </div>
      </div>
    `;
  }

  return { drawRadar, drawMoodChart, renderProgressBars, renderHeatmap, renderReport };
})();
