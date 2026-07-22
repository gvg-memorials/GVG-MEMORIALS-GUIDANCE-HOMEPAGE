(function () {
  const contactForm = document.querySelector('form[name="contact"]');
  const submitButton = contactForm?.querySelector('button[type="submit"]');
  if (!contactForm || !submitButton) return;

  const formStatus = contactForm.querySelector("[data-form-status]");
  const referenceFile = contactForm.querySelector('input[name="reference_file"]');
  const fileHelp = contactForm.querySelector("[data-file-help]");
  const optionalDetails = contactForm.querySelector(".contact-form-details");
  const startingPoint = contactForm.querySelector('select[name="starting_point"]');
  const phone = contactForm.querySelector('input[name="phone"]');
  const message = contactForm.querySelector('textarea[name="message"]');
  const defaultFileHelp = fileHelp?.textContent.trim() || "";
  const defaultSubmitLabel = submitButton.textContent.trim();
  const draftStorageKey = "gvg_contact_draft_v1";
  const draftFieldNames = ["name", "phone", "email", "starting_point", "cemetery", "message"];
  let draftSaveTimer;
  contactForm.noValidate = true;

  const getDraftField = (name) => contactForm.elements.namedItem(name);

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
        window.sessionStorage.setItem(draftStorageKey, JSON.stringify({ values, guidancePrefills }));
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

    if (
      optionalDetails &&
      ["email", "starting_point", "cemetery", "message"].some((name) => getDraftField(name)?.value)
    ) {
      optionalDetails.open = true;
    }
  };

  restoreDraft();
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
      if (optionalDetails) optionalDetails.open = true;
      updateGuidancePrefill(startingPoint, link.dataset.guidanceStartingPoint || "");
      updateGuidancePrefill(message, link.dataset.guidanceMessage || "");
      saveDraft();
    });
  });

  const getErrorElement = (field) => {
    const errorTarget = field.dataset.errorTarget;
    return errorTarget ? document.getElementById(errorTarget) : null;
  };

  const showFormStatus = () => {
    if (!formStatus) return;
    formStatus.textContent = "Please review the highlighted field before sending.";
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
    error.textContent = field.dataset.validationMessage || field.validationMessage;
    error.hidden = false;
  };

  const clearFieldError = (field) => {
    field.removeAttribute("aria-invalid");
    const error = getErrorElement(field);
    if (!error) return;
    error.hidden = true;
    error.textContent = "";
  };

  const updatePhoneValidity = () => {
    if (!phone) return;
    const digitCount = phone.value.replace(/\D/g, "").length;
    phone.setCustomValidity(phone.value.trim() && digitCount < 7 ? "Please enter at least 7 digits." : "");
  };

  phone?.addEventListener("input", updatePhoneValidity);

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

    updatePhoneValidity();
    if (!contactForm.checkValidity()) {
      event.preventDefault();
      contactForm.querySelector("input:invalid, select:invalid, textarea:invalid")?.focus();
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
