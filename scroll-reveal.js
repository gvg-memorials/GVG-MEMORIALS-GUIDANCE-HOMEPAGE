(function () {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const selectors = [
    ".intro .section-label",
    ".intro h2",
    ".intro-copy p",
    ".proof-row span",
    ".credibility article",
    ".memorials .section-heading > *",
    ".memorial-list article",
    ".completed-gallery .section-heading > *",
    ".completed-card",
    ".process .section-heading > *",
    ".steps li",
    ".breathing-content > *",
    ".families-grid > div",
    ".families-notes span",
    ".gallery-image",
    ".gallery-copy > *",
    ".resources .section-heading > *",
    ".resource-list article",
    ".contact-panel > div",
    ".contact-form-grid .field",
    ".contact-form-actions",
  ];

  const elements = selectors.flatMap((selector) => Array.from(document.querySelectorAll(selector)));
  if (!elements.length) return;

  elements.forEach((element, index) => {
    element.setAttribute("data-reveal", element.classList.contains("gallery-image") ? "image" : "soft");
    element.style.setProperty("--reveal-delay", `${Math.min(index % 6, 5) * 70}ms`);
  });

  if (reducedMotion || !("IntersectionObserver" in window)) {
    elements.forEach((element) => element.classList.add("is-visible"));
    return;
  }

  document.body.classList.add("reveal-ready");

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

  const observer = new IntersectionObserver(
    (entries) => {
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

  elements.forEach((element) => observer.observe(element));
  scheduleAnchorReveal();
  window.addEventListener("hashchange", scheduleAnchorReveal);
  window.addEventListener("gvg:anchor-navigate", scheduleAnchorReveal);
})();
