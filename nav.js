(function () {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("mobile-nav");
  if (!toggle || !nav) return;

  const body = document.body;
  const focusableSelector = 'a[href], button:not([disabled])';
  let previouslyFocused = null;

  function openNav() {
    previouslyFocused = document.activeElement;
    nav.hidden = false;
    requestAnimationFrame(() => {
      nav.setAttribute("data-open", "true");
      nav.querySelector(focusableSelector)?.focus();
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
    if (previouslyFocused instanceof HTMLElement) {
      previouslyFocused.focus();
    }
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

    if (event.key !== "Tab" || toggle.getAttribute("aria-expanded") !== "true") {
      return;
    }

    const focusable = Array.from(nav.querySelectorAll(focusableSelector)).filter(
      (element) => element instanceof HTMLElement && element.offsetParent !== null,
    );
    if (!focusable.length) return;

    const first = focusable[0];
    const last = focusable[focusable.length - 1];

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  const desktopBreakpoint = window.matchMedia("(min-width: 921px)");
  desktopBreakpoint.addEventListener("change", (event) => {
    if (event.matches && toggle.getAttribute("aria-expanded") === "true") {
      closeNav();
    }
  });
})();
