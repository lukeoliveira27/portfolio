const T = window.I18N || { pause: 'Pausar vídeo', play: 'Tocar vídeo', zoom: 'Ampliar' };
const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Borda no menu ao rolar
const nav = document.querySelector('.nav');
addEventListener('scroll', () => nav.classList.toggle('is-scrolled', scrollY > 8), { passive: true });

// Entrada suave dos blocos
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  });
}, { rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('.case, .reel__item, .card, .about, .section__head, .step, .cs').forEach((el) => {
  el.classList.add('reveal');
  io.observe(el);
});

// Vídeos: tocam só quando aparecem, com botão de pausa.
// Quem pediu menos movimento no sistema começa com tudo pausado.
const ICON_PAUSE = '<svg viewBox="0 0 16 16" aria-hidden="true"><rect x="3" y="2" width="3.5" height="12" rx="1"/><rect x="9.5" y="2" width="3.5" height="12" rx="1"/></svg>';
const ICON_PLAY = '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5v11a1 1 0 0 0 1.5.86l9-5.5a1 1 0 0 0 0-1.72l-9-5.5A1 1 0 0 0 4 2.5z"/></svg>';
const vio = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    const v = e.target;
    if (e.isIntersecting && !v.dataset.userPaused) v.play().catch(() => {});
    else v.pause();
  });
});
document.querySelectorAll('video').forEach((v) => {
  const box = v.closest('figure') || v.parentElement;
  box.classList.add('has-video');
  const btn = document.createElement('button');
  btn.type = 'button';
  btn.className = 'vbtn';
  const sync = () => {
    const playing = !v.dataset.userPaused;
    btn.innerHTML = playing ? ICON_PAUSE : ICON_PLAY;
    btn.setAttribute('aria-label', playing ? T.pause : T.play);
  };
  if (calm) v.dataset.userPaused = '1';
  btn.addEventListener('click', (ev) => {
    ev.stopPropagation();
    if (v.dataset.userPaused) { delete v.dataset.userPaused; v.play().catch(() => {}); }
    else { v.dataset.userPaused = '1'; v.pause(); }
    sync();
  });
  sync();
  box.appendChild(btn);
  vio.observe(v);
});

// Lightbox
const box = document.querySelector('.lightbox');
const boxImg = box.querySelector('img');
document.querySelectorAll('.zoom').forEach((fig) => {
  const img = fig.querySelector('img');
  if (!img) return;
  fig.tabIndex = 0;
  fig.setAttribute('role', 'button');
  fig.setAttribute('aria-label', `${T.zoom}: ${img.alt}`);
  const open = () => { boxImg.src = img.src; boxImg.alt = img.alt; box.showModal(); };
  fig.addEventListener('click', open);
  fig.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
});
box.addEventListener('click', (e) => { if (e.target !== boxImg) box.close(); });
