// Audio player — replaces the native controls with theme-styled ones.
// Progressive enhancement: the markup ships with `controls`, so without JS
// the native player stays fully usable. We only take over once we're running.
(function () {
  const ICON_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><polygon points="7,4 20,12 7,20" /></svg>';
  const ICON_PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="4" width="4" height="16" /><rect x="14" y="4" width="4" height="16" /></svg>';

  function fmt(seconds) {
    if (!isFinite(seconds)) return '–:––';
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return m + ':' + String(s).padStart(2, '0');
  }

  function enhance(audio) {
    audio.removeAttribute('controls');

    const ui = document.createElement('div');
    ui.className = 'audio-ui';
    ui.innerHTML =
      '<button class="audio-ui__toggle" type="button" aria-label="Abspielen">' + ICON_PLAY + '</button>' +
      '<span class="audio-ui__time"><span class="audio-ui__pos">0:00</span> / <span class="audio-ui__dur">–:––</span></span>' +
      '<div class="audio-ui__track" role="slider" tabindex="0" aria-label="Position im Beitrag"' +
      ' aria-valuemin="0" aria-valuemax="100" aria-valuenow="0"><div class="audio-ui__fill"></div></div>';
    audio.parentNode.insertBefore(ui, audio.nextSibling);

    const toggle = ui.querySelector('.audio-ui__toggle');
    const pos = ui.querySelector('.audio-ui__pos');
    const dur = ui.querySelector('.audio-ui__dur');
    const track = ui.querySelector('.audio-ui__track');
    const fill = ui.querySelector('.audio-ui__fill');

    function paint() {
      const ratio = audio.duration ? audio.currentTime / audio.duration : 0;
      fill.style.width = (ratio * 100) + '%';
      pos.textContent = fmt(audio.currentTime);
      track.setAttribute('aria-valuenow', Math.round(ratio * 100));
    }

    function showDuration() { dur.textContent = fmt(audio.duration); }
    if (audio.readyState >= 1) showDuration();
    audio.addEventListener('loadedmetadata', showDuration);

    toggle.addEventListener('click', () => {
      if (audio.paused) { audio.play(); } else { audio.pause(); }
    });

    audio.addEventListener('play', () => {
      toggle.innerHTML = ICON_PAUSE;
      toggle.setAttribute('aria-label', 'Pause');
      ui.classList.add('is-playing');
    });
    audio.addEventListener('pause', () => {
      toggle.innerHTML = ICON_PLAY;
      toggle.setAttribute('aria-label', 'Abspielen');
      ui.classList.remove('is-playing');
    });
    audio.addEventListener('timeupdate', paint);
    audio.addEventListener('ended', paint);

    function seekTo(clientX) {
      if (!audio.duration) return;
      const box = track.getBoundingClientRect();
      const ratio = Math.min(1, Math.max(0, (clientX - box.left) / box.width));
      audio.currentTime = ratio * audio.duration;
      paint();
    }
    track.addEventListener('click', (e) => seekTo(e.clientX));

    // Keyboard: arrows jump 10s, space toggles — the slider is focusable.
    track.addEventListener('keydown', (e) => {
      if (!audio.duration) return;
      if (e.key === 'ArrowRight') { audio.currentTime = Math.min(audio.duration, audio.currentTime + 10); e.preventDefault(); }
      else if (e.key === 'ArrowLeft') { audio.currentTime = Math.max(0, audio.currentTime - 10); e.preventDefault(); }
      else if (e.key === ' ' || e.key === 'Enter') { audio.paused ? audio.play() : audio.pause(); e.preventDefault(); }
      paint();
    });

    paint();
  }

  function init() {
    document.querySelectorAll('.article-audio__el').forEach(enhance);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
