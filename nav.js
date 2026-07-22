(function () {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("mobile-nav");
  if (!header || !toggle || !nav) return;

  const body = document.body;
  const focusableSelector = 'a[href], button:not([disabled])';
  let previouslyFocused = null;
  let headerUpdatePending = false;

  const mobileContactBar = document.querySelector(".mobile-contact-bar");
  const contactBarBlockers = [
    document.querySelector(".hero"),
    document.querySelector(".contact"),
    document.querySelector(".site-footer"),
  ].filter(Boolean);

  if (mobileContactBar && contactBarBlockers.length && "IntersectionObserver" in window) {
    body.classList.add("mobile-contact-bar-enhanced");
    const visibleBlockers = new Set();

    const contactBarObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleBlockers.add(entry.target);
          } else {
            visibleBlockers.delete(entry.target);
          }
        });

        mobileContactBar.classList.toggle("is-visible", visibleBlockers.size === 0);
      },
      { threshold: 0.01 },
    );

    contactBarBlockers.forEach((element) => contactBarObserver.observe(element));
  }

  function updateHeaderSurface() {
    header.classList.toggle("site-header--solid", window.scrollY > 80);
    headerUpdatePending = false;
  }

  updateHeaderSurface();
  window.addEventListener(
    "scroll",
    () => {
      if (headerUpdatePending) return;
      headerUpdatePending = true;
      window.requestAnimationFrame(updateHeaderSurface);
    },
    { passive: true },
  );

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

  function closeNav(options = {}) {
    const { restoreFocus = true } = options;
    nav.removeAttribute("data-open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Open menu");
    body.classList.remove("nav-open");
    setTimeout(() => {
      if (toggle.getAttribute("aria-expanded") === "false") {
        nav.hidden = true;
      }
    }, 240);
    if (restoreFocus && previouslyFocused instanceof HTMLElement) {
      previouslyFocused.focus();
    }
    previouslyFocused = null;
  }

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    if (isOpen) closeNav();
    else openNav();
  });

  nav.addEventListener("click", (event) => {
    const target = event.target;
    if (target instanceof HTMLAnchorElement) {
      closeNav({ restoreFocus: false });
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
      closeNav({ restoreFocus: false });
    }
  });
})();
