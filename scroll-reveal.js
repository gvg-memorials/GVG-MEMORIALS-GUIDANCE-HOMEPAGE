(function () {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const selectors = [
    ".intro .section-heading > *",
    ".proof-row span",
    ".credibility article",
    ".memorials .section-heading > *",
    ".memorial-list article",
    ".completed-gallery .section-heading > *",
    ".completed-card",
    ".process .section-heading > *",
    ".steps li",
    ".process-note > *",
    ".resources .section-heading > *",
    ".resource-list article",
    ".contact-panel > div",
    ".contact-form-grid .field",
    ".contact-form-actions",
  ];

  const elements = selectors.flatMap((selector) => Array.from(document.querySelectorAll(selector)));
  if (!elements.length) return;

  elements.forEach((element, index) => {
    element.setAttribute("data-reveal", "soft");
    element.style.setProperty("--reveal-delay", `${Math.min(index % 6, 5) * 70}ms`);
  });

  if (reducedMotion || !("IntersectionObserver" in window)) {
    return;
  }

  const revealAnchorTarget = () => {
    if (!window.location.hash) return;

    let target;
    try {
      target = document.querySelector(window.location.hash);
    } catch (_) {
      return;
    }

    if (!target) return;
    if (target === document.body || target.id === "main-content") return;

    [target, ...target.querySelectorAll("[data-reveal]")]
      .filter((element) => element.matches("[data-reveal]"))
      .forEach((element) => {
        element.setAttribute("data-reveal-instant", "");
        element.style.setProperty("--reveal-delay", "0ms");
        element.classList.add("is-visible");
      });
  };

  const scheduleAnchorReveal = () => {
    revealAnchorTarget();
    window.requestAnimationFrame(revealAnchorTarget);
    window.setTimeout(revealAnchorTarget, 240);
  };

  let observer;
  let observerResponded = false;
  let observerWatchdog;
  try {
    observer = new IntersectionObserver(
      (entries) => {
        observerResponded = true;
        window.clearTimeout(observerWatchdog);
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        });
      },
      {
        rootMargin: "0px 0px -12% 0px",
        threshold: 0.12,
      },
    );

    document.documentElement.classList.add("js-reveal");
    elements.forEach((element) => observer.observe(element));
    observerWatchdog = window.setTimeout(() => {
      if (observerResponded) return;
      document.documentElement.classList.remove("js-reveal");
      observer.disconnect();
    }, 1500);
  } catch (_) {
    document.documentElement.classList.remove("js-reveal");
    if (observer) observer.disconnect();
    return;
  }

  scheduleAnchorReveal();
  window.addEventListener("hashchange", scheduleAnchorReveal);
  window.addEventListener("gvg:anchor-navigate", scheduleAnchorReveal);
})();
