// ── Mobile nav toggle ─────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileNav = document.getElementById('mobile-nav');

if (hamburger && mobileNav) {
  hamburger.addEventListener('click', () => {
    mobileNav.classList.toggle('open');
  });
}

// ── Highlight active nav link ──────────────────────────────
document.querySelectorAll('.nav-link, .mobile-nav a').forEach(link => {
  if (link.href === window.location.href) {
    link.style.color = 'var(--blue-light)';
  }
});

// ── Animate service cards on scroll ──────────────────────
if ('IntersectionObserver' in window) {
  const cards = document.querySelectorAll('.service-card, .why-card');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        entry.target.style.transitionDelay = `${(i % 3) * 80}ms`;
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(24px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
  });
}
