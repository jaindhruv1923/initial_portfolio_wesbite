/* ===========================
   app.js — KidLearn
   Main Application Logic
   =========================== */

const App = (() => {

  let currentView = 'parent'; // 'parent' | 'child'
  let toastTimeout = null;

  /* ========================
     INIT
     ======================== */
  function init() {
    applySettings();
    setupAvatarPickers();

    const data = Storage.getData();
    if (!data.children.length) {
      showSplash();
    } else {
      launchApp();
    }
  }

  function applySettings() {
    const s = Storage.getSettings();
    if (s.darkMode) document.documentElement.setAttribute('data-theme', 'dark');
    const soundBtn = document.getElementById('soundBtn');
    if (soundBtn) soundBtn.querySelector('i').className = s.sound ? 'fa fa-volume-up' : 'fa fa-volume-mute';
  }

  /* ========================
     SPLASH / ONBOARDING
     ======================== */
  function showSplash() {
    document.getElementById('splashScreen').classList.remove('hidden');
  }

  function showOnboarding() {
    document.getElementById('splashScreen').classList.add('hidden');
    document.getElementById('onboardingScreen').classList.remove('hidden');
  }

  function completeOnboarding() {
    const parentName = document.getElementById('parentNameInput').value.trim();
    const childName  = document.getElementById('childNameInput').value.trim();
    const childAge   = document.getElementById('childAgeInput').value;
    const avatar     = document.querySelector('#avatarPicker .avatar-opt.selected')?.dataset.val || '🦁';

    if (!parentName || !childName) { showToast('⚠️ Please fill in all fields!'); return; }

    Storage.setParent(parentName);
    Storage.addChild(childName, childAge, avatar);

    document.getElementById('onboardingScreen').classList.add('hidden');
    launchApp();
  }

  /* ========================
     LAUNCH
     ======================== */
  function launchApp() {
    document.getElementById('splashScreen').classList.add('hidden');
    document.getElementById('onboardingScreen').classList.add('hidden');
    document.getElementById('mainApp').classList.remove('hidden');

    renderProfileSwitcher();
    renderSubjects();
    renderNotesSubjects();
    
    const params = new URLSearchParams(window.location.search);
    const targetPage = params.get('page') || 'dashboard';
    navigate(targetPage);
    Timer.init();
  }

  /* ========================
     NAVIGATION
     ======================== */
  function navigate(page) {
    document.querySelectorAll('.page').forEach(p => {
      p.classList.add('hidden');
      p.classList.remove('active');
    });
    const el = document.getElementById(`page-${page}`);
    if (el) { el.classList.remove('hidden'); el.classList.add('active'); }

    document.querySelectorAll('.nav-item').forEach(n => {
      n.classList.toggle('active', n.dataset.page === page);
    });

    const titles = {
      dashboard: 'Dashboard', subjects: 'Subjects', timer: 'Focus Timer',
      achievements: 'Badges', goals: 'Goals', notes: 'Notes',
      report: 'Report Card', heatmap: 'Heatmap',
    };
    document.getElementById('pageTitle').textContent = titles[page] || page;

    const child = Storage.getActiveChild();
    if (!child) return;

    switch (page) {
      case 'dashboard':    refreshDashboard(); break;
      case 'achievements': Achievements.renderBadgesGrid(child); break;
      case 'goals':        renderGoals(child); break;
      case 'report':       Charts.renderReport(child); break;
      case 'heatmap':      Charts.renderHeatmap(child); break;
      case 'notes':        renderNotes(child); break;
      case 'timer':        Timer.updateUI(); break;
    }

    // Close sidebar on mobile
    if (window.innerWidth <= 768) {
      document.getElementById('sidebar').classList.remove('open');
    }
  }

  /* ========================
     DASHBOARD REFRESH
     ======================== */
  function refreshDashboard() {
    const child = Storage.getActiveChild();
    if (!child) return;

    // Welcome banner
    const banner = document.getElementById('welcomeBanner');
    const hour   = new Date().getHours();
    const greet  = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening';
    banner.innerHTML = `
      <div>
        <div class="welcome-title">${greet}, ${child.name}! ${child.avatar}</div>
        <div class="welcome-sub">Keep up the great work · Level ${Math.floor(child.xp / 100) + 1}</div>
      </div>
    `;

    // Stats
    document.getElementById('statXP').textContent      = child.xp;
    document.getElementById('statStreak').textContent  = child.streak;
    document.getElementById('statLessons').textContent = Object.values(child.subjects).reduce((s, v) => s + v.lessons, 0);
    document.getElementById('statBadges').textContent  = (child.badges || []).length;
    document.getElementById('topXP').textContent       = child.xp;
    document.getElementById('topStreak').textContent   = child.streak;

    // Charts
    Charts.renderProgressBars(child);
    Charts.drawRadar(child);
    Charts.drawMoodChart(child);
    Achievements.renderRecentBadges(child);
  }

  /* ========================
     PROFILE SWITCHER
     ======================== */
  function renderProfileSwitcher() {
    const el = document.getElementById('profileSwitcher');
    const data = Storage.getData();
    el.innerHTML = data.children.map(c => `
      <button class="profile-child-btn ${c.id === data.activeChildId ? 'active' : ''}"
        onclick="App.switchChild('${c.id}')">
        <span class="profile-avatar">${c.avatar}</span>
        <div class="profile-info">
          <div class="profile-name">${c.name}</div>
          <div class="profile-age">Age ${c.age}</div>
        </div>
      </button>
    `).join('');
  }

  function switchChild(id) {
    Storage.setActiveChild(id);
    renderProfileSwitcher();
    renderSubjects();
    renderNotesSubjects();
    navigate('dashboard');
  }

  /* ========================
     SUBJECTS
     ======================== */
  function renderSubjects() {
    const el = document.getElementById('subjectsGrid');
    if (!el) return;
    const child = Storage.getActiveChild();
    if (!child) return;

    const XP_PER_LESSON = 20;
    el.innerHTML = Object.entries(child.subjects).map(([name, data]) => `
      <div class="subject-card hover-lift">
        <div class="subject-emoji">${data.emoji}</div>
        <div class="subject-name">${name}</div>
        <div class="subject-lessons">${data.lessons} lessons completed</div>
        <div class="subject-xp-badge">+${XP_PER_LESSON} XP per lesson</div>
        <button class="subject-complete-btn" onclick="App.completeLesson('${name}')">
          ✅ Complete Lesson
        </button>
      </div>
    `).join('');
  }

  function completeLesson(subject) {
    const child = Storage.getActiveChild();
    if (!child) return;

    const XP = 20;
    Storage.completeLesson(child.id, subject, XP);
    showToast(`🎉 ${subject} lesson done! +${XP} XP`);
    showXPPopup(XP);
    playAchievementSound();

    const updated = Storage.getActiveChild();
    const newBadges = Achievements.checkAndAward(updated);
    if (newBadges.length) handleNewBadges(newBadges);

    renderSubjects();
    refreshDashboard();
  }

  /* ========================
     MOOD
     ======================== */
  function logMood(mood) {
    const child = Storage.getActiveChild();
    if (!child) return;
    Storage.logMood(child.id, mood);

    document.querySelectorAll('.mood-btn').forEach(b => {
      b.classList.toggle('selected', parseInt(b.dataset.mood) === mood);
    });
    showToast('💭 Mood logged!');
    Charts.drawMoodChart(Storage.getActiveChild());
  }

  /* ========================
     GOALS
     ======================== */
  function renderGoals(child) {
    const el = document.getElementById('goalsList');
    if (!el) return;
    const goals = child.goals || [];
    if (!goals.length) {
      el.innerHTML = '<div class="empty-state"><div class="empty-state-icon">🎯</div><div class="empty-state-title">No goals yet</div><div class="empty-state-sub">Add a weekly goal below</div></div>';
      return;
    }
    el.innerHTML = goals.map((g, i) => {
      const pct = Math.min(Math.round((g.current / g.target) * 100), 100);
      const subj = child.subjects[g.subject];
      return `
        <div class="goal-item">
          <div class="goal-subject">${subj?.emoji || '📚'} ${g.subject}</div>
          <div class="goal-progress-mini">
            <div class="progress-track">
              <div class="progress-fill" style="width:${pct}%;background:${subj?.color || '#6C63FF'}"></div>
            </div>
          </div>
          <div class="goal-numbers">${g.current}/${g.target}</div>
          <button class="goal-delete" onclick="App.deleteGoal(${i})">×</button>
        </div>
      `;
    }).join('');
  }

  function addGoal() {
    const subject = document.getElementById('goalSubjectInput').value.trim();
    const target  = document.getElementById('goalTargetInput').value;
    const child   = Storage.getActiveChild();
    if (!child || !subject || !target) { showToast('⚠️ Fill in subject and target!'); return; }
    if (!child.subjects[subject]) { showToast(`⚠️ Subject "${subject}" not found`); return; }
    Storage.addGoal(child.id, subject, target);
    document.getElementById('goalSubjectInput').value = '';
    document.getElementById('goalTargetInput').value  = '';
    renderGoals(Storage.getActiveChild());
    showToast('🎯 Goal added!');
  }

  function deleteGoal(index) {
    const child = Storage.getActiveChild();
    if (!child) return;
    Storage.removeGoal(child.id, index);
    renderGoals(Storage.getActiveChild());
  }

  /* ========================
     NOTES
     ======================== */
  function renderNotesSubjects() {
    const list   = document.getElementById('notesSubjectList');
    const select = document.getElementById('notesSubjectSelect');
    const child  = Storage.getActiveChild();
    if (!list || !child) return;

    const subjects = Object.entries(child.subjects);
    list.innerHTML = subjects.map(([name, data]) => `
      <button class="notes-subject-btn" onclick="App.selectNoteSubject('${name}')">${data.emoji} ${name}</button>
    `).join('');

    if (select) {
      select.innerHTML = subjects.map(([name, data]) =>
        `<option value="${name}">${data.emoji} ${name}</option>`
      ).join('');
    }
  }

  function renderNotes(child) {
    const first = Object.keys(child.subjects)[0];
    if (first) selectNoteSubject(first);
  }

  function selectNoteSubject(subject) {
    const child = Storage.getActiveChild();
    if (!child) return;
    const area   = document.getElementById('notesArea');
    const select = document.getElementById('notesSubjectSelect');
    if (area) area.value = child.notes?.[subject] || '';
    if (select) select.value = subject;

    document.querySelectorAll('.notes-subject-btn').forEach(b => {
      b.classList.toggle('active', b.textContent.includes(subject));
    });
  }

  function saveNote() {
    const child   = Storage.getActiveChild();
    const subject = document.getElementById('notesSubjectSelect')?.value;
    const text    = document.getElementById('notesArea')?.value || '';
    if (!child || !subject) return;
    Storage.saveNote(child.id, subject, text);
    showToast('📝 Note saved!');

    const newBadges = Achievements.checkAndAward(Storage.getActiveChild());
    if (newBadges.length) handleNewBadges(newBadges);
  }

  /* ========================
     ADD CHILD MODAL
     ======================== */
  function addChild() {
    document.getElementById('addChildModal').classList.remove('hidden');
    setupAvatarPickers();
  }

  function closeModal() {
    document.getElementById('addChildModal').classList.add('hidden');
  }

  function saveNewChild() {
    const name   = document.getElementById('newChildName').value.trim();
    const age    = document.getElementById('newChildAge').value;
    const avatar = document.querySelector('#addAvatarPicker .avatar-opt.selected')?.dataset.val || '🦁';
    if (!name) { showToast('⚠️ Enter child name!'); return; }
    Storage.addChild(name, age, avatar);
    closeModal();
    renderProfileSwitcher();
    renderSubjects();
    showToast(`🎉 ${name} added!`);
  }

  /* ========================
     VIEW TOGGLE
     ======================== */
  function setView(view) {
    currentView = view;
    document.body.classList.toggle('child-view', view === 'child');
    document.getElementById('btnParentView').classList.toggle('active', view === 'parent');
    document.getElementById('btnChildView').classList.toggle('active', view === 'child');

    // Hide parent-only elements in child view
    const parentOnly = document.querySelectorAll('.parent-only');
    parentOnly.forEach(el => el.style.display = (view === 'child') ? 'none' : '');
  }

  /* ========================
     DARK MODE & SOUND
     ======================== */
  function toggleDark() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    Storage.setSetting('darkMode', !isDark);
    // Redraw charts with new theme colours
    const child = Storage.getActiveChild();
    if (child) { Charts.drawRadar(child); Charts.drawMoodChart(child); }
  }

  function toggleSound() {
    const s = Storage.getSettings();
    Storage.setSetting('sound', !s.sound);
    const btn = document.getElementById('soundBtn');
    if (btn) btn.querySelector('i').className = !s.sound ? 'fa fa-volume-up' : 'fa fa-volume-mute';
    showToast(s.sound ? '🔇 Sound off' : '🔊 Sound on');
  }

  /* ========================
     SIDEBAR TOGGLE
     ======================== */
  function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const main    = document.querySelector('.main-content');
    if (window.innerWidth <= 768) {
      sidebar.classList.toggle('open');
    } else {
      sidebar.classList.toggle('collapsed');
      main.classList.toggle('expanded');
    }
  }

  /* ========================
     BADGES
     ======================== */
  function handleNewBadges(badgeIds) {
    badgeIds.forEach((id, i) => {
      const badge = Achievements.getById(id);
      if (!badge) return;
      setTimeout(() => {
        showToast(`🏅 New badge: ${badge.emoji} ${badge.name}!`);
        Achievements.spawnConfetti();
        playAchievementSound();
      }, i * 800);
    });
  }

  /* ========================
     AVATAR PICKERS
     ======================== */
  function setupAvatarPickers() {
    document.querySelectorAll('.avatar-picker').forEach(picker => {
      picker.querySelectorAll('.avatar-opt').forEach(opt => {
        opt.addEventListener('click', () => {
          picker.querySelectorAll('.avatar-opt').forEach(o => o.classList.remove('selected'));
          opt.classList.add('selected');
        });
      });
    });
  }

  /* ========================
     TOAST
     ======================== */
  function showToast(msg) {
    const el = document.getElementById('toast');
    if (!el) return;
    el.textContent = msg;
    el.classList.remove('hidden');
    clearTimeout(toastTimeout);
    toastTimeout = setTimeout(() => el.classList.add('hidden'), 3000);
  }

  /* ========================
     XP POPUP
     ======================== */
  function showXPPopup(amount) {
    const el = document.createElement('div');
    el.className = 'xp-popup';
    el.textContent = `+${amount} XP ⚡`;
    el.style.left = `${Math.random() * 60 + 20}%`;
    el.style.top  = `${Math.random() * 30 + 40}%`;
    document.body.appendChild(el);
    setTimeout(() => el.remove(), 1300);
  }

  /* ========================
     SOUND
     ======================== */
  function playAchievementSound() {
    if (!Storage.getSettings().sound) return;
    try {
      const ctx  = new (window.AudioContext || window.webkitAudioContext)();
      const osc  = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      osc.type = 'sine';
      osc.frequency.setValueAtTime(440, ctx.currentTime);
      osc.frequency.setValueAtTime(554, ctx.currentTime + 0.1);
      osc.frequency.setValueAtTime(659, ctx.currentTime + 0.2);
      gain.gain.setValueAtTime(0.25, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.5);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.5);
    } catch (e) { /* ignore */ }
  }

  /* ========================
     EXPOSE & AUTO-INIT
     ======================== */
  document.addEventListener('DOMContentLoaded', init);

  return {
    init, showOnboarding, completeOnboarding, navigate, switchChild,
    completeLesson, logMood, addGoal, deleteGoal, saveNote,
    selectNoteSubject, addChild, closeModal, saveNewChild,
    setView, toggleDark, toggleSound, toggleSidebar,
    refreshDashboard, handleNewBadges, showToast, showXPPopup,
  };
})();
