// Borda no menu ao rolar
const nav = document.querySelector('.nav');
addEventListener('scroll', () => nav.classList.toggle('is-scrolled', scrollY > 8), { passive: true });

// Entrada suave dos blocos
const io = new IntersectionObserver((entries) => {
  entries.forEach((e) => {
    if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
  });
}, { rootMargin: '0px 0px -10% 0px' });
document.querySelectorAll('.case, .reel__item, .card, .about, .section__head').forEach((el) => {
  el.classList.add('reveal');
  io.observe(el);
});

// Vídeos só tocam quando aparecem na tela
const vio = new IntersectionObserver((entries) => {
  entries.forEach((e) => (e.isIntersecting ? e.target.play().catch(() => {}) : e.target.pause()));
});
document.querySelectorAll('video').forEach((v) => vio.observe(v));

// Lightbox
const box = document.querySelector('.lightbox');
const boxImg = box.querySelector('img');
document.querySelectorAll('.zoom').forEach((fig) => {
  fig.tabIndex = 0;
  fig.setAttribute('role', 'button');
  const img = fig.querySelector('img');
  fig.setAttribute('aria-label', `Ampliar: ${img.alt}`);
  const open = () => { boxImg.src = img.src; boxImg.alt = img.alt; box.showModal(); };
  fig.addEventListener('click', open);
  fig.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); } });
});
box.addEventListener('click', (e) => { if (e.target !== boxImg) box.close(); });
