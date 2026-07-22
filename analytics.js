(function () {
  const productionHosts = new Set(["gvgmemorials.com", "www.gvgmemorials.com"]);
  if (!productionHosts.has(window.location.hostname) || typeof window.gtag !== "function") return;

  const measurementId = "G-JSMJEPF8ZV";
  const consentStorageKey = "gvg_analytics_consent";
  let analyticsRequested = false;

  const readConsent = () => {
    try {
      return window.localStorage.getItem(consentStorageKey);
    } catch (_) {
      return null;
    }
  };

  const saveConsent = (value) => {
    try {
      window.localStorage.setItem(consentStorageKey, value);
    } catch (_) {
      // The choice still applies to this page when storage is unavailable.
    }
  };

  let consentState = readConsent();

  function loadGoogleAnalytics() {
    if (analyticsRequested) return;
    analyticsRequested = true;
    window.gtag("config", measurementId, {
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
    });

    const script = document.createElement("script");
    script.async = true;
    script.src = `https://www.googletagmanager.com/gtag/js?id=${measurementId}`;
    document.head.append(script);
  }

  if (consentState === "granted") {
    loadGoogleAnalytics();
  }

  const sendEvent = (name, parameters) => {
    if (consentState !== "granted") return;
    loadGoogleAnalytics();
    window.gtag("event", name, {
      transport_type: "beacon",
      ...parameters,
    });
  };

  const consentBanner = document.querySelector("[data-analytics-consent]");
  const consentAccept = document.querySelector("[data-analytics-accept]");
  const consentDecline = document.querySelector("[data-analytics-decline]");
  const consentChoiceButtons = document.querySelectorAll("[data-analytics-choices]");
  let consentReturnTarget = null;

  const showConsentChoices = (trigger) => {
    if (!consentBanner) return;
    if (trigger instanceof HTMLElement) consentReturnTarget = trigger;
    consentChoiceButtons.forEach((button) => button.setAttribute("aria-expanded", "true"));
    consentBanner.hidden = false;
    window.requestAnimationFrame(() => consentBanner.classList.add("is-visible"));
  };

  const hideConsentChoices = () => {
    if (!consentBanner) return;
    const returnTarget = consentReturnTarget;
    consentReturnTarget = null;
    consentChoiceButtons.forEach((button) => button.setAttribute("aria-expanded", "false"));
    consentBanner.classList.remove("is-visible");
    window.setTimeout(() => {
      consentBanner.hidden = true;
      if (returnTarget?.isConnected) {
        returnTarget.focus({ preventScroll: true });
      }
    }, 220);
  };

  const updateConsent = (value) => {
    consentState = value;
    saveConsent(value);
    window.gtag("consent", "update", {
      analytics_storage: value,
      ad_storage: "denied",
      ad_user_data: "denied",
      ad_personalization: "denied",
    });
    if (value === "granted") {
      loadGoogleAnalytics();
    }
    hideConsentChoices();
  };

  if (consentBanner && consentState === null) {
    showConsentChoices();
  }

  consentAccept?.addEventListener("click", () => updateConsent("granted"));
  consentDecline?.addEventListener("click", () => updateConsent("denied"));
  consentChoiceButtons.forEach((button) => {
    button.addEventListener("click", () => {
      showConsentChoices(button);
      window.setTimeout(() => consentAccept?.focus(), 40);
    });
  });
  consentBanner?.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    event.preventDefault();
    hideConsentChoices();
  });

  const getLocation = (element) => {
    if (element.closest(".mobile-contact-bar")) return "mobile_contact_bar";
    if (element.closest(".mobile-nav")) return "mobile_navigation";
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

    if (link.classList.contains("completed-card-trigger")) {
      const card = link.closest(".completed-card");
      sendEvent("gallery_image_open", {
        gallery_category: card?.querySelector("figcaption span")?.textContent.trim() || "completed_memorial",
        gallery_item: card?.querySelector("figcaption strong")?.textContent.trim() || "memorial_detail",
      });
      return;
    }

    if (link.dataset.analyticsEvent === "reviews_click") {
      sendEvent("reviews_click", { contact_location: location });
      return;
    }

    if (link.dataset.analyticsEvent === "directions_click") {
      sendEvent("directions_click", { contact_location: location });
      return;
    }

    if (link.dataset.analyticsEvent === "appointment_click") {
      sendEvent("appointment_click", { contact_location: location });
      return;
    }

    if (href.startsWith("tel:")) {
      sendEvent("phone_click", { contact_location: location });
      return;
    }

    if (href.startsWith("mailto:")) {
      sendEvent("email_click", { contact_location: location });
      return;
    }

    if (href === "#contact" || href === "#contact-form") {
      sendEvent("guidance_cta_click", {
        cta_location: location,
        guidance_item: link.dataset.guidanceItem || "general_guidance",
      });
    }
  });

  document.querySelectorAll(".faq-list details").forEach((details) => {
    details.addEventListener("toggle", () => {
      if (!details.open) return;
      sendEvent("faq_open", {
        faq_question: details.querySelector("summary")?.textContent.trim() || "family_question",
      });
    });
  });

  window.addEventListener("gvg:gallery-navigate", (event) => {
    const detail = event.detail || {};
    sendEvent("gallery_image_open", {
      gallery_category: detail.category?.trim() || "completed_memorial",
      gallery_item: detail.item?.trim() || "memorial_detail",
      gallery_navigation: detail.navigation || "viewer",
    });
  });

  window.addEventListener("gvg:gallery-inquiry", (event) => {
    const detail = event.detail || {};
    sendEvent("gallery_inquiry_click", {
      gallery_category: detail.category?.trim() || "completed_memorial",
      gallery_item: detail.item?.trim() || "memorial_detail",
    });
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
      const invalidFields = Array.from(contactForm.querySelectorAll(":invalid"))
        .map((field) => field.getAttribute("name"))
        .filter(Boolean);
      const phone = contactForm.querySelector('input[name="phone"]');
      const phoneDigitCount = phone ? phone.value.replace(/\D/g, "").length : 0;
      if (phone?.value.trim() && phoneDigitCount < 7 && !invalidFields.includes("phone")) {
        invalidFields.push("phone");
      }

      if (invalidFields.length) {
        sendEvent("contact_form_validation_error", {
          form_name: "contact",
          invalid_fields: invalidFields.join(","),
        });
        return;
      }

      sendEvent("contact_form_submit", { form_name: "contact" });
      try {
        window.sessionStorage.setItem("gvg_contact_submitted", "true");
      } catch (_) {
        // The form still works when browser storage is unavailable.
      }
    });

    const referenceFile = contactForm.querySelector('input[name="reference_file"]');
    referenceFile?.addEventListener("change", () => {
      const file = referenceFile.files?.[0];
      if (!file) return;
      sendEvent("contact_file_added", {
        form_name: "contact",
        file_type: file.type || "unknown",
      });
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
