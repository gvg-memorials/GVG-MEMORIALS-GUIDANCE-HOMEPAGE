(function () {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("mobile-nav");
  if (!toggle || !nav) return;

  const body = document.body;

  function openNav() {
    nav.hidden = false;
    requestAnimationFrame(() => {
      nav.setAttribute("data-open", "true");
    });
    toggle.setAttribute("aria-expanded", "true");
    toggle.setAttribute("aria-label", "Close menu");
    body.classList.add("nav-open");
  }

  function closeNav() {
    nav.removeAttribute("data-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    body.classList.remove("nav-open");
    setTimeout(() => {
      if (toggle.getAttribute("aria-expanded") === "false") {
        nav.hidden = true;
      }
    }, 240);
  }

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    if (isOpen) closeNav();
    else openNav();
  });

  nav.addEventListener("click", (event) => {
    const target = event.target;
    if (target instanceof HTMLAnchorElement) {
      closeNav();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      closeNav();
      toggle.focus();
    }
  });

  const desktopBreakpoint = window.matchMedia("(min-width: 921px)");
  desktopBreakpoint.addEventListener("change", (event) => {
    if (event.matches && toggle.getAttribute("aria-expanded") === "true") {
      closeNav();
    }
  });
})();
