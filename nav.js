(function () {
  const header = document.querySelector(".site-header");
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("mobile-nav");
  if (!header || !toggle || !nav) return;

  const body = document.body;
  const focusableSelector = 'a[href], button:not([disabled])';
  const navTransitionDuration = 240;
  const backgroundRegions = [
    document.getElementById("main-content"),
    document.querySelector(".site-footer"),
    document.querySelector(".analytics-consent"),
  ].filter(Boolean);
  const backgroundRegionStates = new Map();
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
    const contactBarLinks = Array.from(mobileContactBar.querySelectorAll("a[href]"));
    const originalTabIndexes = new Map(
      contactBarLinks.map((link) => [link, link.getAttribute("tabindex")]),
    );

    const setContactBarVisibility = (isVisible) => {
      mobileContactBar.classList.toggle("is-visible", isVisible);

      if (isVisible) {
        mobileContactBar.removeAttribute("aria-hidden");
        mobileContactBar.removeAttribute("inert");
        contactBarLinks.forEach((link) => {
          const originalTabIndex = originalTabIndexes.get(link);
          if (originalTabIndex === null) {
            link.removeAttribute("tabindex");
          } else {
            link.setAttribute("tabindex", originalTabIndex);
          }
        });
        return;
      }

      mobileContactBar.setAttribute("aria-hidden", "true");
      mobileContactBar.setAttribute("inert", "");
      contactBarLinks.forEach((link) => link.setAttribute("tabindex", "-1"));
    };

    setContactBarVisibility(false);

    const contactBarObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleBlockers.add(entry.target);
          } else {
            visibleBlockers.delete(entry.target);
          }
        });

        setContactBarVisibility(visibleBlockers.size === 0);
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

  function setNavigationBackgroundHidden(isHidden) {
    backgroundRegions.forEach((region) => {
      if (isHidden) {
        if (!backgroundRegionStates.has(region)) {
          backgroundRegionStates.set(region, {
            ariaHidden: region.getAttribute("aria-hidden"),
            inert: region.hasAttribute("inert"),
          });
        }
        region.setAttribute("aria-hidden", "true");
        region.setAttribute("inert", "");
        return;
      }

      const originalState = backgroundRegionStates.get(region);
      if (!originalState) return;

      if (originalState.ariaHidden === null) {
        region.removeAttribute("aria-hidden");
      } else {
        region.setAttribute("aria-hidden", originalState.ariaHidden);
      }

      if (!originalState.inert) {
        region.removeAttribute("inert");
      }
      backgroundRegionStates.delete(region);
    });
  }

  function focusHashTarget(hash, delay = 80) {
    if (!hash || hash === "#") return;

    let targetId;
    try {
      targetId = decodeURIComponent(hash.slice(1));
    } catch {
      return;
    }

    const target = document.getElementById(targetId);
    if (!target) return;

    const focusTarget = target.matches("h1, h2, h3, [tabindex]")
      ? target
      : target.querySelector("h1, h2, h3") || target;
    const originalTabIndex = focusTarget.getAttribute("tabindex");

    if (originalTabIndex === null) {
      focusTarget.setAttribute("tabindex", "-1");
    }

    setTimeout(() => {
      focusTarget.focus({ preventScroll: true });
      if (originalTabIndex === null) {
        focusTarget.addEventListener(
          "blur",
          () => focusTarget.removeAttribute("tabindex"),
          { once: true },
        );
      }
    }, delay);
  }

  function openNav() {
    previouslyFocused = document.activeElement;
    nav.hidden = false;
    setNavigationBackgroundHidden(true);
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
        setNavigationBackgroundHidden(false);
      }
    }, navTransitionDuration);
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
      focusHashTarget(target.hash, navTransitionDuration + 20);
    }
  });

  document.addEventListener("click", (event) => {
    const origin = event.target instanceof Element ? event.target : null;
    const link = origin?.closest('a[href^="#"]');
    if (
      !link ||
      link.closest("#mobile-nav") ||
      link.classList.contains("memorial-viewer-inquiry")
    ) {
      return;
    }

    focusHashTarget(link.hash);
  });

  if (window.location.hash) {
    window.addEventListener(
      "load",
      () => focusHashTarget(window.location.hash, 600),
      { once: true },
    );
  }

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
