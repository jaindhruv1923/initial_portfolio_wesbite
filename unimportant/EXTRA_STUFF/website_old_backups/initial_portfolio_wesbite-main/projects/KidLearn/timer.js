/* ===========================
   timer.js — KidLearn
   Pomodoro Focus Timer
   =========================== */

const Timer = (() => {
  const FOCUS_SECS = 25 * 60;
  const BREAK_SECS = 5 * 60;
  const CIRCUMFERENCE = 2 * Math.PI * 88; // r=88

  let remaining = FOCUS_SECS;
  let isRunning = false;
  let isBreak   = false;
  let interval  = null;

  function fmt(secs) {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = (secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
  }

  function updateUI() {
    const display = document.getElementById('timerDisplay');
    const arc     = document.getElementById('timerArc');
    const label   = document.getElementById('timerLabel');
    const btn     = document.getElementById('timerStartBtn');
    const count   = document.getElementById('pomodoroCount');

    if (!display) return;

    const total    = isBreak ? BREAK_SECS : FOCUS_SECS;
    const progress = remaining / total;
    const offset   = CIRCUMFERENCE * (1 - progress);

    display.textContent = fmt(remaining);
    if (arc) {
      arc.style.strokeDashoffset = offset;
      arc.className = `timer-progress${isBreak ? ' break-mode' : ''}`;
    }
    if (label) {
      if (!isRunning && remaining === (isBreak ? BREAK_SECS : FOCUS_SECS)) {
        label.textContent = isBreak ? '☕ Take a break!' : 'Ready to focus?';
      } else if (isBreak) {
        label.textContent = '☕ Break time — stretch a bit!';
      } else {
        label.textContent = '🎯 Stay focused!';
      }
    }
    if (btn) btn.textContent = isRunning ? '⏸ Pause' : '▶ Start';

    // Sync pomodoro count
    const child = Storage.getActiveChild();
    if (count && child) {
      const today = new Date().toDateString();
      const todayPomodoros = child.lastPomodoroDate === today ? child.pomodorosToday : 0;
      count.textContent = todayPomodoros || 0;
    }
  }

  function tick() {
    if (remaining <= 0) {
      clearInterval(interval);
      isRunning = false;

      if (!isBreak) {
        // Focus session done
        const child = Storage.getActiveChild();
        if (child) {
          Storage.incrementPomodoro(child.id);
          App.showToast('🍅 Focus session done! +50 XP');
          App.showXPPopup(50);
          Storage.completeLesson(child.id, '_pomodoro', 50);
          const newBadges = Achievements.checkAndAward(Storage.getActiveChild());
          if (newBadges.length) App.handleNewBadges(newBadges);
        }
        isBreak = true;
        remaining = BREAK_SECS;
        if (Storage.getSettings().sound) playSound('break');
      } else {
        // Break done
        isBreak = false;
        remaining = FOCUS_SECS;
        App.showToast('✅ Break over! Ready to focus again?');
        if (Storage.getSettings().sound) playSound('focus');
      }

      App.refreshDashboard();
    } else {
      remaining--;
    }
    updateUI();
  }

  function toggle() {
    if (isRunning) {
      clearInterval(interval);
      isRunning = false;
    } else {
      interval = setInterval(tick, 1000);
      isRunning = true;
    }
    updateUI();
  }

  function reset() {
    clearInterval(interval);
    isRunning = false;
    isBreak   = false;
    remaining = FOCUS_SECS;
    updateUI();
  }

  function playSound(type) {
    try {
      const ctx = new (window.AudioContext || window.webkitAudioContext)();
      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);
      if (type === 'break') {
        osc.frequency.setValueAtTime(523, ctx.currentTime);
        osc.frequency.setValueAtTime(659, ctx.currentTime + 0.15);
        osc.frequency.setValueAtTime(784, ctx.currentTime + 0.3);
      } else {
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        osc.frequency.setValueAtTime(550, ctx.currentTime + 0.15);
      }
      gain.gain.setValueAtTime(0.3, ctx.currentTime);
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
      osc.start(ctx.currentTime);
      osc.stop(ctx.currentTime + 0.6);
    } catch (e) { /* AudioContext not available */ }
  }

  function init() { updateUI(); }

  return { toggle, reset, init, updateUI };
})();
