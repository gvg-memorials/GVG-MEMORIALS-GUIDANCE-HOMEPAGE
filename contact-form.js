(function () {
  const contactForm = document.querySelector('form[name="contact"]');
  const submitButton = contactForm?.querySelector('button[type="submit"]');
  if (!contactForm || !submitButton) return;

  const formStatus = contactForm.querySelector("[data-form-status]");
  const referenceFile = contactForm.querySelector('input[name="reference_file"]');
  const fileHelp = contactForm.querySelector("[data-file-help]");
  const optionalDetails = contactForm.querySelector(".contact-form-details");
  const startingPoint = contactForm.querySelector('select[name="starting_point"]');
  const message = contactForm.querySelector('textarea[name="message"]');
  const defaultFileHelp = fileHelp?.textContent.trim() || "";
  const defaultSubmitLabel = submitButton.textContent.trim();
  contactForm.noValidate = true;

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

    if (!contactForm.checkValidity()) {
      event.preventDefault();
      contactForm.querySelector("input:invalid, select:invalid, textarea:invalid")?.focus();
      return;
    }

    if (formStatus) {
      formStatus.hidden = true;
      formStatus.textContent = "";
    }
    submitButton.disabled = true;
    submitButton.setAttribute("aria-busy", "true");
    submitButton.textContent = "Sending...";
  });

  window.addEventListener("pageshow", resetSubmitButton);
})();
