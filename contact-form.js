(function () {
  const contactForm = document.querySelector('form[name="contact"]');
  const submitButton = contactForm?.querySelector('button[type="submit"]');
  if (!contactForm || !submitButton) return;

  const formStatus = contactForm.querySelector("[data-form-status]");
  const referenceFile = contactForm.querySelector('input[name="reference_file"]');
  const fileHelp = contactForm.querySelector("[data-file-help]");
  const optionalDetails = contactForm.querySelector(".contact-form-details");
  const guidanceContext = contactForm.querySelector("[data-guidance-context]");
  const guidanceContextText = contactForm.querySelector("[data-guidance-context-text]");
  const guidanceContextReview = contactForm.querySelector("[data-guidance-context-review]");
  const startingPoint = contactForm.querySelector('select[name="starting_point"]');
  const name = contactForm.querySelector('input[name="name"]');
  const phone = contactForm.querySelector('input[name="phone"]');
  const email = contactForm.querySelector('input[name="email"]');
  const message = contactForm.querySelector('textarea[name="message"]');
  const defaultFileHelp = fileHelp?.textContent.trim() || "";
  const defaultSubmitLabel = submitButton.textContent.trim();
  const attributionStorageKey = "gvg_contact_attribution_v1";
  const attributionFieldNames = [
    "traffic_source",
    "landing_path",
    "referrer_host",
    "utm_source",
    "utm_medium",
    "utm_campaign",
  ];
  const draftStorageKey = "gvg_contact_draft_v1";
  const draftFieldNames = ["name", "phone", "email", "starting_point", "cemetery", "message"];
  let guidanceContextValue = "";
  let draftSaveTimer;
  contactForm.noValidate = true;

  const getDraftField = (name) => contactForm.elements.namedItem(name);

  const hasVisitorOptionalDetails = () => {
    const visitorTextFields = ["cemetery"];
    const hasVisitorText = visitorTextFields.some((fieldName) => getDraftField(fieldName)?.value.trim());
    const hasEditedGuidance = [startingPoint, message].some(
      (field) => field?.value.trim() && field.value !== field.dataset.guidancePrefill,
    );
    return hasVisitorText || hasEditedGuidance || Boolean(referenceFile?.files?.length);
  };

  const setGuidanceContext = (value, collapseDetails = true) => {
    guidanceContextValue = typeof value === "string" ? value.trim().slice(0, 180) : "";
    if (!guidanceContext || !guidanceContextText) return;

    guidanceContextText.textContent = guidanceContextValue;
    guidanceContext.hidden = !guidanceContextValue;
    if (guidanceContextValue && collapseDetails && optionalDetails) {
      optionalDetails.open = hasVisitorOptionalDetails();
    }
  };

  const syncGuidanceReviewControl = () => {
    if (!guidanceContextReview || !optionalDetails) return;
    const detailsOpen = optionalDetails.open;
    guidanceContextReview.hidden = detailsOpen;
    guidanceContextReview.setAttribute("aria-expanded", String(detailsOpen));
  };

  optionalDetails?.addEventListener("toggle", syncGuidanceReviewControl);

  const setAttributionFields = () => {
    const searchParams = new URLSearchParams(window.location.search);
    let referrerHost = "";
    try {
      const referrerUrl = new URL(document.referrer);
      if (referrerUrl.origin !== window.location.origin) referrerHost = referrerUrl.hostname;
    } catch (_) {
      // Direct visits and privacy-restricted referrers have no usable host.
    }

    const currentAttribution = {
      traffic_source: searchParams.get("utm_source") || referrerHost || "direct",
      landing_path: window.location.pathname,
      referrer_host: referrerHost,
      utm_source: searchParams.get("utm_source") || "",
      utm_medium: searchParams.get("utm_medium") || "",
      utm_campaign: searchParams.get("utm_campaign") || "",
    };
    let attribution = currentAttribution;

    try {
      const storedAttribution = JSON.parse(window.sessionStorage.getItem(attributionStorageKey) || "null");
      if (storedAttribution && typeof storedAttribution === "object") {
        attribution = storedAttribution;
      } else {
        window.sessionStorage.setItem(attributionStorageKey, JSON.stringify(currentAttribution));
      }
    } catch (_) {
      // Attribution still applies to this submission when session storage is unavailable.
    }

    attributionFieldNames.forEach((fieldName) => {
      const field = contactForm.elements.namedItem(fieldName);
      const value = attribution[fieldName];
      if (field instanceof HTMLInputElement && typeof value === "string") {
        field.value = value.slice(0, 120);
      }
    });
  };

  setAttributionFields();

  const saveDraft = () => {
    const values = {};
    const guidancePrefills = {};

    draftFieldNames.forEach((name) => {
      const field = getDraftField(name);
      if (!(field instanceof HTMLInputElement || field instanceof HTMLSelectElement || field instanceof HTMLTextAreaElement)) {
        return;
      }

      if (field.value) values[name] = field.value;
      if (field.dataset.guidancePrefill) guidancePrefills[name] = field.dataset.guidancePrefill;
    });

    try {
      if (Object.keys(values).length) {
        window.sessionStorage.setItem(
          draftStorageKey,
          JSON.stringify({ values, guidancePrefills, guidanceContext: guidanceContextValue }),
        );
      } else {
        window.sessionStorage.removeItem(draftStorageKey);
      }
    } catch (_) {
      // The form remains fully usable when session storage is unavailable.
    }
  };

  const scheduleDraftSave = () => {
    window.clearTimeout(draftSaveTimer);
    draftSaveTimer = window.setTimeout(saveDraft, 180);
  };

  const restoreDraft = () => {
    let draft;
    try {
      draft = JSON.parse(window.sessionStorage.getItem(draftStorageKey) || "null");
    } catch (_) {
      return;
    }
    if (!draft?.values || typeof draft.values !== "object") return;

    draftFieldNames.forEach((name) => {
      const field = getDraftField(name);
      const value = draft.values[name];
      if (
        !(field instanceof HTMLInputElement || field instanceof HTMLSelectElement || field instanceof HTMLTextAreaElement) ||
        typeof value !== "string" ||
        field.value
      ) {
        return;
      }

      if (field instanceof HTMLSelectElement && !Array.from(field.options).some((option) => option.value === value)) {
        return;
      }

      field.value = field.maxLength > 0 ? value.slice(0, field.maxLength) : value;
      if (draft.guidancePrefills?.[name] === value) {
        field.dataset.guidancePrefill = value;
      }
    });

    if (typeof draft.guidanceContext === "string" && draft.guidanceContext.trim()) {
      setGuidanceContext(draft.guidanceContext);
    } else if (
      optionalDetails &&
      ["starting_point", "cemetery", "message"].some((name) => getDraftField(name)?.value)
    ) {
      optionalDetails.open = true;
    }
  };

  restoreDraft();
  syncGuidanceReviewControl();
  contactForm.addEventListener("input", scheduleDraftSave);
  contactForm.addEventListener("change", scheduleDraftSave);
  window.addEventListener("pagehide", saveDraft);

  const updateGuidancePrefill = (field, value) => {
    if (!field) return;
    const previousPrefill = field.dataset.guidancePrefill || "";
    const currentValue = field.value.trim();
    const canReplace = !currentValue || (previousPrefill && field.value === previousPrefill);
    if (!canReplace) return;

    field.value = value;
    if (value) {
      field.dataset.guidancePrefill = value;
    } else {
      delete field.dataset.guidancePrefill;
    }
  };

  document.querySelectorAll("[data-guidance-starting-point]").forEach((link) => {
    link.addEventListener("click", () => {
      const openDetails = link.dataset.guidanceOpenDetails === "true";
      updateGuidancePrefill(startingPoint, link.dataset.guidanceStartingPoint || "");
      updateGuidancePrefill(message, link.dataset.guidanceMessage || "");
      setGuidanceContext(
        link.dataset.guidanceItem || link.dataset.guidanceStartingPoint || "",
        !openDetails,
      );
      if (openDetails && optionalDetails) {
        optionalDetails.open = true;
      }
      saveDraft();
    });
  });

  window.addEventListener("gvg:guidance-selected", (event) => {
    setGuidanceContext(event.detail?.item || "");
    saveDraft();
  });

  guidanceContextReview?.addEventListener("click", () => {
    if (!optionalDetails) return;
    optionalDetails.open = true;
    optionalDetails.querySelector("summary")?.focus();
  });

  const getErrorElement = (field) => {
    const errorTarget = field.dataset.errorTarget;
    return errorTarget ? document.getElementById(errorTarget) : null;
  };

  const getFieldValidationMessage = (field) => {
    if (field.validity.valueMissing) {
      if (field.getAttribute("name") === "name") return "Please enter your name.";
    }

    if (field.getAttribute("name") === "phone" && field.validity.customError) {
      return field.validationMessage;
    }

    return (
      field.dataset.validationMessage ||
      field.validationMessage ||
      "Please review the highlighted field before sending."
    );
  };

  const showFormStatus = () => {
    if (!formStatus) return;
    const invalidFields = Array.from(
      contactForm.querySelectorAll("input:invalid, select:invalid, textarea:invalid"),
    );
    const invalidNames = new Set(invalidFields.map((field) => field.getAttribute("name")));

    if (
      invalidNames.has("name") &&
      invalidNames.has("phone") &&
      !phone?.value.trim() &&
      !email?.value.trim()
    ) {
      formStatus.textContent = "Please enter your name and a phone number or email address.";
    } else if (invalidFields.length === 1) {
      formStatus.textContent = getFieldValidationMessage(invalidFields[0]);
    } else {
      formStatus.textContent = "Please review the highlighted fields before sending.";
    }
    formStatus.hidden = false;
  };

  const updateFormStatus = () => {
    if (!formStatus) return;
    const hasVisibleError =
      contactForm.querySelector('.field-error:not([hidden])') ||
      contactForm.querySelector("[data-file-help].is-error");
    if (hasVisibleError) return;
    formStatus.hidden = true;
    formStatus.textContent = "";
  };

  const showFieldError = (field) => {
    field.setAttribute("aria-invalid", "true");
    const error = getErrorElement(field);
    if (!error) return;
    error.textContent = getFieldValidationMessage(field);
    error.hidden = false;
  };

  const clearFieldError = (field) => {
    field.removeAttribute("aria-invalid");
    const error = getErrorElement(field);
    if (!error) return;
    error.hidden = true;
    error.textContent = "";
  };

  const updateContactMethodValidity = () => {
    if (!phone) return;
    const digitCount = phone.value.replace(/\D/g, "").length;
    let message = "";
    if (!phone.value.trim() && !email?.value.trim()) {
      message = "Please enter a phone number or email address.";
    } else if (phone.value.trim() && digitCount < 7) {
      message = "Please enter a phone number with at least 7 digits.";
    }
    phone.setCustomValidity(message);
    if (!message) {
      clearFieldError(phone);
      updateFormStatus();
    }
  };

  phone?.addEventListener("input", updateContactMethodValidity);
  email?.addEventListener("input", updateContactMethodValidity);
  name?.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.isComposing || !phone) return;
    event.preventDefault();
    phone.focus();
  });

  contactForm.addEventListener(
    "invalid",
    (event) => {
      const field = event.target;
      if (!(field instanceof HTMLInputElement || field instanceof HTMLSelectElement || field instanceof HTMLTextAreaElement)) {
        return;
      }
      showFieldError(field);
      showFormStatus();
    },
    true,
  );

  const clearValidField = (event) => {
    const field = event.target;
    if (!(field instanceof HTMLInputElement || field instanceof HTMLSelectElement || field instanceof HTMLTextAreaElement)) {
      return;
    }
    if (!field.validity.valid) return;
    clearFieldError(field);
    updateFormStatus();
  };

  contactForm.addEventListener("input", clearValidField);
  contactForm.addEventListener("change", clearValidField);

  if (referenceFile && fileHelp) {
    const maxFileSize = 8 * 1024 * 1024;

    referenceFile.addEventListener("change", () => {
      const file = referenceFile.files?.[0];
      referenceFile.setCustomValidity("");
      referenceFile.removeAttribute("aria-invalid");
      fileHelp.classList.remove("is-error");
      fileHelp.textContent = defaultFileHelp;

      if (!file || file.size <= maxFileSize) {
        updateFormStatus();
        return;
      }

      const message = "Please choose a file smaller than 8 MB.";
      referenceFile.setCustomValidity(message);
      referenceFile.setAttribute("aria-invalid", "true");
      fileHelp.classList.add("is-error");
      fileHelp.textContent = message;
      showFormStatus();
      referenceFile.reportValidity();
    });
  }

  const resetSubmitButton = () => {
    submitButton.disabled = false;
    submitButton.removeAttribute("aria-busy");
    submitButton.textContent = defaultSubmitLabel;
  };

  contactForm.addEventListener("submit", (event) => {
    if (submitButton.disabled) {
      event.preventDefault();
      return;
    }

    updateContactMethodValidity();
    if (!contactForm.checkValidity()) {
      event.preventDefault();
      const firstInvalidField = contactForm.querySelector(
        "input:invalid, select:invalid, textarea:invalid",
      );
      firstInvalidField?.focus({ preventScroll: true });
      const invalidScrollTarget =
        firstInvalidField === name || firstInvalidField === phone
          ? contactForm
          : firstInvalidField?.closest(".field") || firstInvalidField || contactForm;
      invalidScrollTarget.scrollIntoView({
        behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",
        block: "start",
      });
      return;
    }

    if (formStatus) {
      formStatus.hidden = true;
      formStatus.textContent = "";
    }
    try {
      window.sessionStorage.setItem("gvg_contact_draft_submitted", "true");
    } catch (_) {
      // Successful submission does not depend on session storage.
    }
    submitButton.disabled = true;
    submitButton.setAttribute("aria-busy", "true");
    submitButton.textContent = "Sending...";
  });

  window.addEventListener("pageshow", resetSubmitButton);
})();
