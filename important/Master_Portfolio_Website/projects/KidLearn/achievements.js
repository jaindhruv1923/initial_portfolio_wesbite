/* ===========================
   achievements.js — KidLearn
   Badge definitions & checks
   =========================== */

const Achievements = (() => {

  const BADGES = [
    { id: 'first_lesson',    emoji: '🌟', name: 'First Step',      desc: 'Complete your first lesson' },
    { id: 'streak_3',        emoji: '🔥', name: '3 Day Streak',    desc: 'Learn 3 days in a row' },
    { id: 'streak_7',        emoji: '🚀', name: '7 Day Streak',    desc: 'Learn 7 days in a row' },
    { id: 'streak_30',       emoji: '💎', name: '30 Day Streak',   desc: 'Learn 30 days in a row' },
    { id: 'math_champ',      emoji: '🔢', name: 'Math Champion',   desc: 'Complete 10 Math lessons' },
    { id: 'bookworm',        emoji: '📚', name: 'Bookworm',        desc: 'Complete 10 Reading lessons' },
    { id: 'scientist',       emoji: '🔬', name: 'Scientist',       desc: 'Complete 10 Science lessons' },
    { id: 'historian',       emoji: '🏛️', name: 'Historian',      desc: 'Complete 10 History lessons' },
    { id: 'wordsmith',       emoji: '✏️', name: 'Wordsmith',       desc: 'Complete 10 English lessons' },
    { id: 'artist',          emoji: '🎨', name: 'Artist',          desc: 'Complete 10 Art lessons' },
    { id: 'xp_100',          emoji: '⚡', name: 'XP Hunter',       desc: 'Earn 100 XP' },
    { id: 'xp_500',          emoji: '💥', name: 'XP Warrior',      desc: 'Earn 500 XP' },
    { id: 'xp_1000',         emoji: '🏆', name: 'XP Legend',       desc: 'Earn 1000 XP' },
    { id: 'early_bird',      emoji: '🌅', name: 'Early Bird',      desc: 'Study before 9 AM' },
    { id: 'night_owl',       emoji: '🦉', name: 'Night Owl',       desc: 'Study after 8 PM' },
    { id: 'all_rounder',     emoji: '🌈', name: 'All Rounder',     desc: 'Complete at least 1 lesson in every subject' },
    { id: 'pomodoro_5',      emoji: '🍅', name: 'Focus Master',    desc: 'Complete 5 Pomodoro sessions' },
    { id: 'goal_achiever',   emoji: '🎯', name: 'Goal Achiever',   desc: 'Complete a weekly goal' },
    { id: 'note_taker',      emoji: '📝', name: 'Note Taker',      desc: 'Write notes in 3 subjects' },
    { id: 'lessons_25',      emoji: '🎖️', name: 'Lesson Master',  desc: 'Complete 25 total lessons' },
    { id: 'lessons_50',      emoji: '👑', name: 'Grand Scholar',   desc: 'Complete 50 total lessons' },
  ];

  function getAll() { return BADGES; }

  function getById(id) { return BADGES.find(b => b.id === id); }

  function checkAndAward(child) {
    const newBadges = [];
    const earned = child.badges || [];
    const totalLessons = Object.values(child.subjects).reduce((s, v) => s + v.lessons, 0);
    const hour = new Date().getHours();

    const checks = [
      { id: 'first_lesson',  cond: totalLessons >= 1 },
      { id: 'streak_3',      cond: child.streak >= 3 },
      { id: 'streak_7',      cond: child.streak >= 7 },
      { id: 'streak_30',     cond: child.streak >= 30 },
      { id: 'math_champ',    cond: (child.subjects.Math?.lessons || 0) >= 10 },
      { id: 'bookworm',      cond: (child.subjects.Reading?.lessons || 0) >= 10 },
      { id: 'scientist',     cond: (child.subjects.Science?.lessons || 0) >= 10 },
      { id: 'historian',     cond: (child.subjects.History?.lessons || 0) >= 10 },
      { id: 'wordsmith',     cond: (child.subjects.English?.lessons || 0) >= 10 },
      { id: 'artist',        cond: (child.subjects.Art?.lessons || 0) >= 10 },
      { id: 'xp_100',        cond: child.xp >= 100 },
      { id: 'xp_500',        cond: child.xp >= 500 },
      { id: 'xp_1000',       cond: child.xp >= 1000 },
      { id: 'early_bird',    cond: hour < 9 && totalLessons > 0 },
      { id: 'night_owl',     cond: hour >= 20 && totalLessons > 0 },
      { id: 'all_rounder',   cond: Object.values(child.subjects).every(s => s.lessons >= 1) },
      { id: 'pomodoro_5',    cond: (child.pomodorosToday || 0) >= 5 },
      { id: 'goal_achiever', cond: (child.goals || []).some(g => g.current >= g.target) },
      { id: 'note_taker',    cond: Object.keys(child.notes || {}).filter(k => child.notes[k]?.trim()).length >= 3 },
      { id: 'lessons_25',    cond: totalLessons >= 25 },
      { id: 'lessons_50',    cond: totalLessons >= 50 },
    ];

    checks.forEach(({ id, cond }) => {
      if (cond && !earned.includes(id)) {
        Storage.addBadge(child.id, id);
        newBadges.push(id);
      }
    });

    return newBadges;
  }

  function renderBadgesGrid(child) {
    const grid = document.getElementById('badgesGrid');
    if (!grid) return;
    const earned = child.badges || [];
    const total = BADGES.length;
    const earnedCount = earned.length;

    document.getElementById('badgeProgress').textContent =
      `${earnedCount} / ${total} badges earned`;

    grid.innerHTML = BADGES.map(b => {
      const isEarned = earned.includes(b.id);
      return `
        <div class="badge-card ${isEarned ? 'earned' : 'locked'} hover-lift">
          ${isEarned ? '<div class="badge-earned-tag">✓ Earned</div>' : ''}
          <div class="badge-emoji">${b.emoji}</div>
          <div class="badge-name">${b.name}</div>
          <div class="badge-desc">${b.desc}</div>
        </div>
      `;
    }).join('');
  }

  function renderRecentBadges(child) {
    const el = document.getElementById('recentBadges');
    if (!el) return;
    const earned = (child.badges || []).slice(-6);
    if (!earned.length) {
      el.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🏅</div><div class="empty-state-sub">Complete lessons to earn badges!</div></div>';
      return;
    }
    el.innerHTML = earned.map(id => {
      const b = getById(id);
      if (!b) return '';
      return `<div class="badge-mini"><span>${b.emoji}</span><span class="badge-mini-name">${b.name}</span></div>`;
    }).join('');
  }

  function spawnConfetti() {
    const colors = ['#6C63FF','#FF6584','#43D9AD','#FF9F43','#48DBFB'];
    for (let i = 0; i < 18; i++) {
      const el = document.createElement('div');
      el.className = 'confetti-piece';
      el.style.cssText = `
        left: ${Math.random() * 100}vw;
        top: ${Math.random() * 40}vh;
        background: ${colors[Math.floor(Math.random()*colors.length)]};
        animation-delay: ${Math.random() * 0.6}s;
        animation-duration: ${0.9 + Math.random() * 0.6}s;
      `;
      document.body.appendChild(el);
      setTimeout(() => el.remove(), 1500);
    }
  }

  return { getAll, getById, checkAndAward, renderBadgesGrid, renderRecentBadges, spawnConfetti };
})();
