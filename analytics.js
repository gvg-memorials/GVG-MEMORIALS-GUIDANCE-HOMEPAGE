(function () {
  const productionHosts = new Set(["gvgmemorials.com", "www.gvgmemorials.com"]);
  if (!productionHosts.has(window.location.hostname) || typeof window.gtag !== "function") return;

  const measurementId = "G-JSMJEPF8ZV";
  const interactionEvents = ["pointerdown", "touchstart", "keydown"];
  let analyticsRequested = false;
  let loadTimer;

  const scheduleAnalytics = () => {
    if (!analyticsRequested) {
      loadTimer = window.setTimeout(loadGoogleAnalytics, 4000);
    }
  };

  function loadGoogleAnalytics() {
    if (analyticsRequested) return;
    analyticsRequested = true;
    window.clearTimeout(loadTimer);
    window.removeEventListener("load", scheduleAnalytics);
    interactionEvents.forEach((eventName) => {
      window.removeEventListener(eventName, loadGoogleAnalytics);
    });

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.append(script);
  }

  interactionEvents.forEach((eventName) => {
    window.addEventListener(eventName, loadGoogleAnalytics, { once: true, passive: true });
  });

  if (document.readyState === "complete") {
    scheduleAnalytics();
  } else {
    window.addEventListener("load", scheduleAnalytics, { once: true });
  }

  const sendEvent = (name, parameters) => {
    window.gtag("event", name, {
      transport_type: "beacon",
      ...parameters,
    });
  };

  const getLocation = (element) => {
    if (element.closest(".mobile-contact-bar")) return "mobile_contact_bar";
    if (element.closest(".site-header")) return "header";
    if (element.closest(".hero")) return "hero";
    if (element.closest(".contact")) return "contact";
    if (element.closest(".thank-you")) return "thank_you";
    if (element.closest(".site-footer")) return "footer";
    return "page";
  };

  document.addEventListener("click", (event) => {
    const origin = event.target instanceof Element ? event.target : null;
    const link = origin ? origin.closest("a") : null;
    if (!link) return;

    const href = link.getAttribute("href") || "";
    const location = getLocation(link);

    if (href.startsWith("tel:")) {
      sendEvent("phone_click", { contact_location: location });
      return;
    }

    if (href.startsWith("mailto:")) {
      sendEvent("email_click", { contact_location: location });
      return;
    }

    if (href === "#contact" || href === "#contact-form") {
      sendEvent("guidance_cta_click", { cta_location: location });
    }
  });

  const contactForm = document.querySelector('form[name="contact"]');
  if (contactForm) {
    let formStarted = false;
    const trackFormStart = () => {
      if (formStarted) return;
      formStarted = true;
      sendEvent("contact_form_start", { form_name: "contact" });
    };

    contactForm.addEventListener("focusin", trackFormStart);
    contactForm.addEventListener("change", trackFormStart);

    const optionalDetails = contactForm.querySelector(".contact-form-details");
    if (optionalDetails) {
      let detailsOpened = false;
      optionalDetails.addEventListener("toggle", () => {
        if (optionalDetails.open && !detailsOpened) {
          detailsOpened = true;
          sendEvent("contact_details_open", { form_name: "contact" });
        }
      });
    }

    contactForm.addEventListener("submit", () => {
      sendEvent("contact_form_submit", { form_name: "contact" });
      try {
        window.sessionStorage.setItem("gvg_contact_submitted", "true");
      } catch (_) {
        // The form still works when browser storage is unavailable.
      }
    });
  }

  if (window.location.pathname === "/thank-you" || window.location.pathname === "/thank-you.html") {
    try {
      if (window.sessionStorage.getItem("gvg_contact_submitted") === "true") {
        sendEvent("generate_lead", {
          method: "contact_form",
          form_name: "contact",
        });
        window.sessionStorage.removeItem("gvg_contact_submitted");
      }
    } catch (_) {
      // Avoid counting direct thank-you page visits as completed leads.
    }
  }
})();
