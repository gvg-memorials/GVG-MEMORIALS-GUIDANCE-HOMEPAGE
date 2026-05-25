(function () {
  const hero = document.querySelector(".hero");
  if (!hero) return;

  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reducedMotion) {
    hero.style.setProperty("--hero-scroll-progress", "0");
    return;
  }

  let ticking = false;

  function clamp(value, min, max) {
    return Math.min(Math.max(value, min), max);
  }

  function updateHeroProgress() {
    const rect = hero.getBoundingClientRect();
    const progress = clamp(Math.abs(Math.min(rect.top, 0)) / Math.max(rect.height * 0.72, 1), 0, 1);
    hero.style.setProperty("--hero-scroll-progress", progress.toFixed(3));
    ticking = false;
  }

  function requestUpdate() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(updateHeroProgress);
  }

  updateHeroProgress();
  window.addEventListener("scroll", requestUpdate, { passive: true });
  window.addEventListener("resize", requestUpdate);
})();
