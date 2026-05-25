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
    ".process .section-heading > *",
    ".steps li",
    ".breathing-content > *",
    ".families-grid > div",
    ".families-notes span",
    ".gallery-image",
    ".gallery-copy > *",
    ".resources .section-heading > *",
    ".resource-list article",
    ".appointment-grid > div",
    ".appointment-list span",
    ".contact-panel > div",
    ".contact-form-header > *",
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
})();
