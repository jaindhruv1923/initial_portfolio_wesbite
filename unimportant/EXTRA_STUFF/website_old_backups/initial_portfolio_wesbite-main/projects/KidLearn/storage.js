/* ===========================
   storage.js — KidLearn
   Local Storage wrapper
   =========================== */

const Storage = (() => {
  const KEY = 'kidlearn_data';

  const defaults = () => {
    const aarav = {
      id: 'child_aarav',
      name: 'Aarav',
      age: 8,
      avatar: '🦁',
      xp: 1450,
      streak: 7,
      lastActiveDate: new Date().toISOString(),
      subjects: {
        Math:    { emoji: '🔢', lessons: 12, color: '#6C63FF' },
        Reading: { emoji: '📖', lessons: 10, color: '#FF6584' },
        Science: { emoji: '🔬', lessons: 14, color: '#43D9AD' },
        History: { emoji: '🏛️', lessons: 8,  color: '#FF9F43' },
        English: { emoji: '✏️', lessons: 9,  color: '#48DBFB' },
        Art:     { emoji: '🎨', lessons: 6,  color: '#A29BFE' }
      },
      badges: ['first_step', 'curious_mind', 'streak_3', 'streak_7', 'math_wiz', 'bookworm', 'science_exp', 'early_bird', 'pomodoro_pro'],
      goals: [
        { subject: 'Math', target: 15, current: 12 },
        { subject: 'Science', target: 15, current: 14 },
        { subject: 'Reading', target: 12, current: 10 }
      ],
      notes: {
        Math: "Practicing 2-digit multiplication and fractions.",
        Science: "Photosynthesis diagrams and solar system models.",
        Reading: "Chapter 4 of The Magic Treehouse completed!"
      },
      moodLog: [
        { date: 'Mon', mood: '😄', xpThatDay: 180 },
        { date: 'Tue', mood: '😃', xpThatDay: 220 },
        { date: 'Wed', mood: '😐', xpThatDay: 140 },
        { date: 'Thu', mood: '😄', xpThatDay: 260 },
        { date: 'Fri', mood: '🤩', xpThatDay: 310 },
        { date: 'Sat', mood: '😃', xpThatDay: 190 },
        { date: 'Sun', mood: '🤩', xpThatDay: 150 }
      ],
      pomodorosToday: 3,
      lastPomodoroDate: new Date().toISOString(),
      weeklyXP: 450,
      weekStart: new Date().toISOString()
    };
    return {
      parentName: 'Vikram Sharma',
      activeChildId: 'child_aarav',
      children: [aarav],
      settings: { sound: true, darkMode: false },
    };
  };

  const childDefaults = (name, age, avatar) => ({
    id: Date.now().toString(),
    name,
    age: parseInt(age) || 8,
    avatar: avatar || '🦁',
    xp: 0,
    streak: 0,
    lastActiveDate: null,
    subjects: {
      Math:    { emoji: '🔢', lessons: 0, color: '#6C63FF' },
      Reading: { emoji: '📖', lessons: 0, color: '#FF6584' },
      Science: { emoji: '🔬', lessons: 0, color: '#43D9AD' },
      History: { emoji: '🏛️', lessons: 0, color: '#FF9F43' },
      English: { emoji: '✏️', lessons: 0, color: '#48DBFB' },
      Art:     { emoji: '🎨', lessons: 0, color: '#A29BFE' },
    },
    badges: [],         // array of badge ids
    goals: [],          // [{ subject, target, current }]
    notes: {},          // { subject: text }
    moodLog: [],        // [{ date, mood, xpThatDay }]
    pomodorosToday: 0,
    lastPomodoroDate: null,
    weeklyXP: 0,
    weekStart: null,
  });

  /* ---- READ / WRITE ---- */
  function load() {
    try {
      const raw = localStorage.getItem(KEY);
      return raw ? JSON.parse(raw) : defaults();
    } catch { return defaults(); }
  }

  function save(data) {
    try { localStorage.setItem(KEY, JSON.stringify(data)); }
    catch (e) { console.error('Storage save failed:', e); }
  }

  /* ---- PUBLIC API ---- */
  function getData() { return load(); }

  function setParent(name) {
    const d = load();
    d.parentName = name;
    save(d);
  }

  function addChild(name, age, avatar) {
    const d = load();
    const child = childDefaults(name, age, avatar);
    d.children.push(child);
    if (!d.activeChildId) d.activeChildId = child.id;
    save(d);
    return child;
  }

  function getActiveChild() {
    const d = load();
    return d.children.find(c => c.id === d.activeChildId) || d.children[0] || null;
  }

  function setActiveChild(id) {
    const d = load();
    d.activeChildId = id;
    save(d);
  }

  function updateChild(childId, updater) {
    const d = load();
    const idx = d.children.findIndex(c => c.id === childId);
    if (idx === -1) return;
    updater(d.children[idx]);
    save(d);
  }

  function completeLesson(childId, subject, xpAmount) {
    updateChild(childId, child => {
      if (!child.subjects[subject]) return;
      child.subjects[subject].lessons += 1;
      child.xp += xpAmount;
      child.weeklyXP = (child.weeklyXP || 0) + xpAmount;

      // Update streak
      const today = new Date().toDateString();
      if (child.lastActiveDate !== today) {
        const yesterday = new Date(Date.now() - 86400000).toDateString();
        child.streak = (child.lastActiveDate === yesterday) ? (child.streak || 0) + 1 : 1;
        child.lastActiveDate = today;
      }

      // Update goals
      (child.goals || []).forEach(g => {
        if (g.subject === subject) g.current = (g.current || 0) + 1;
      });
    });
  }

  function logMood(childId, mood) {
    updateChild(childId, child => {
      const today = new Date().toDateString();
      const existing = (child.moodLog || []).findIndex(m => m.date === today);
      const entry = { date: today, mood, xpThatDay: child.xp };
      if (existing >= 0) child.moodLog[existing] = entry;
      else child.moodLog.push(entry);
      if (child.moodLog.length > 30) child.moodLog = child.moodLog.slice(-30);
    });
  }

  function addBadge(childId, badgeId) {
    updateChild(childId, child => {
      if (!child.badges.includes(badgeId)) child.badges.push(badgeId);
    });
  }

  function hasBadge(childId, badgeId) {
    const d = load();
    const child = d.children.find(c => c.id === childId);
    return child ? child.badges.includes(badgeId) : false;
  }

  function addGoal(childId, subject, target) {
    updateChild(childId, child => {
      child.goals = child.goals || [];
      child.goals.push({ subject, target: parseInt(target), current: 0 });
    });
  }

  function removeGoal(childId, index) {
    updateChild(childId, child => {
      child.goals.splice(index, 1);
    });
  }

  function saveNote(childId, subject, text) {
    updateChild(childId, child => {
      child.notes = child.notes || {};
      child.notes[subject] = text;
    });
  }

  function incrementPomodoro(childId) {
    updateChild(childId, child => {
      const today = new Date().toDateString();
      if (child.lastPomodoroDate !== today) {
        child.pomodorosToday = 0;
        child.lastPomodoroDate = today;
      }
      child.pomodorosToday = (child.pomodorosToday || 0) + 1;
    });
  }

  function getSettings() { return load().settings || { sound: true, darkMode: false }; }

  function setSetting(key, val) {
    const d = load();
    d.settings = d.settings || {};
    d.settings[key] = val;
    save(d);
  }

  function clearAll() {
    localStorage.removeItem(KEY);
  }

  return {
    getData, setParent, addChild, getActiveChild, setActiveChild,
    updateChild, completeLesson, logMood, addBadge, hasBadge,
    addGoal, removeGoal, saveNote, incrementPomodoro,
    getSettings, setSetting, clearAll,
  };
})();
